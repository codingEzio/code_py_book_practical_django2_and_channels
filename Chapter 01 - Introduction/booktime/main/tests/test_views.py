import sys
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from django.contrib import auth

from main import forms, models


class TestPage(TestCase):
    def test_home_page_works(self):
        """
        Frankly, these comments aren't necessary for me.
        But.. Just in case I forgot this, I'll put some notes in here.

        `assertContains`    Does the page contains strings like 'BookTime'?
        `reverse("home")`   The "home" is the `name` attr in the `urlpatterns`.
        """

        response = self.client.get(reverse("main:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "BookTime")

    def test_about_page_works(self):
        response = self.client.get(reverse("main:about_us"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about_us.html")
        self.assertContains(response, "BookTime")

    def test_contact_us_page_works(self):
        response = self.client.get(reverse("main:contact_us"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact_form.html")
        self.assertContains(response, "BookTime")
        self.assertIsInstance(
            response.context["form"], forms.ContactForm
        )

    def test_products_page_returns_active(self):
        """
        Test links like this
            http://localhost:8000/products/all/
        """

        models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )

        models.Product.objects.create(
            name="A Tale of Two Cities",
            slug="tale-two-cities",
            price=Decimal("2.00"),
            active=False,
        )

        response = self.client.get(
            reverse("main:products", kwargs={ "tag": "all" })
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BookTime")

        product_list = models.Product.objects \
            .active() \
            .order_by("name")

        self.assertEqual(
            list(response.context["object_list"]),
            list(product_list),
        )

    def test_products_page_filters_by_tags_and_active(self):
        """
        Test links like this
            http://localhost:8000/products/opensource/
        """

        cb = models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        cb.tags.create(name="Open Source", slug="opensource")

        models.Product.objects.create(
            name="Microsoft Windows guide",
            slug="microsoft-windows-guide",
            price=Decimal("12.00"),
        )

        # Get the one which its tag is `opensource`
        response = self.client.get(
            reverse("main:products", kwargs={ "tag": "opensource" })
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BookTime")

        # Also,
        # Get the one which its tag is `opensource`
        product_list = (
            models.Product.objects.active() \
                .filter(tags__slug="opensource") \
                .order_by("name")
        )

        # One for 'accessing the page'
        # One for 'checking the database'
        self.assertEqual(
            list(response.context["object_list"]),
            list(product_list),
        )

    def test_user_signup_page_loads_correctly(self):
        """
        """
        response = self.client.get(reverse("main:signup"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertContains(response, "BookTime")
        self.assertIsInstance(
            response.context["form"], forms.UserCreationForm
        )

    def test_user_signup_page_submission_works(self):
        """
        """

        post_data = {
            "email": "user@domain.com",
            "password1": "abcabcabc",
            "password2": "abcabcabc",
        }

        with patch.object(forms.UserCreationForm, "send_mail") as mock_send:
            response = self.client.post(
                reverse("main:signup"), post_data
            )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            models.User.objects.filter(
                email="user@domain.com"
            ).exists()
        )

        self.assertTrue(
            auth.get_user(self.client).is_authenticated
        )

        mock_send.assert_called_once()

    def test_address_list_page_returns_only_owned(self):
        user1 = models.User.objects.create_user(
            "user1", "whatever"
        )
        user2 = models.User.objects.create_user(
            "user2", "whatever"
        )

        models.Address.objects.create(
            user=user1,
            name="jone doe",
            address1="addr One",
            address2="addr Two",
            city="London",
            country="uk",
        )
        models.Address.objects.create(
            user=user2,
            name="jay morse",
            address1="baker st221b",
            address2="baker st222b",
            city="London",
            country="uk",
        )

        self.client.force_login(user2)

        response = self.client.get(reverse("main:address_list"))

        self.assertEqual(response.status_code, 200)

        address_list = models.Address.objects.filter(user=user2)
        self.assertEqual(
            list(response.context["object_list"]),
            list(address_list),
        )

    def test_address_create_stores_user(self):
        user1 = models.User.objects.create_user(
            "user1", "whatever"
        )

        post_data = {
            "name": "john snow",
            "address1": "north land",
            "address2": "",
            "zip_code": "888899",
            "city": "tully",
            "country": "uk",
        }

        self.client.force_login(user1)
        self.client.post(
            reverse("main:address_create"),
            post_data
        )

        self.assertTrue(
            models.Address.objects.filter(user=user1).exists()
        )

    def test_add_to_basket_logged_in_works(self):
        """
        These are what we're testing for
        -- Does the basket able to detect the duplicates (same ID; product still could be bought twice!).
        -- Does the basket able to "remember" the previously added product (1+1 should be 2, XD).
        """

        user1 = models.User.objects.create_user(
            "user1@example.com", "whatever-aha"
        )
        prod1 = models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        prod2 = models.Product.objects.create(
            name="Django2 by example",
            slug="django2-example",
            price=Decimal("29.99"),
        )

        self.client.force_login(user1)

        response = self.client.get(
            reverse("main:add_to_basket"),
            { "product_id": prod1.id }
        )

        # I wonder if this is a typo, which is,
        # this part was written twice in the book (ah).
        response = self.client.get(
            reverse("main:add_to_basket"),
            { "product_id": prod1.id }
        )

        self.assertTrue(
            models.Basket.objects.filter(user=user1).exists()
        )
        self.assertEquals(
            models.BasketLine.objects.filter(
                basket__user=user1
            ).count(),
            1,
        )

        # Pitfall
        #   Mixed 'get(reverse(a), b)' with 'get(reverse(a, b)'
        response = self.client.get(
            reverse("main:add_to_basket"), {"product_id": prod2.id}
        )
        self.assertEquals(
            models.BasketLine.objects.filter(
                basket__user=user1
            ).count(),
            2,
        )