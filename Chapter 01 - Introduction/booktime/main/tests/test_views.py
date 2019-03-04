from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from main import forms, models
import sys


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