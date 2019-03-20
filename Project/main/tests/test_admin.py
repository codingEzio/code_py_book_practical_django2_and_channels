from decimal import Decimal
from datetime import datetime
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from main import factories
from main import models


class TestAdminViews(TestCase):
    def test_most_bought_products(self):
        products = [
            factories.ProductFactory(name="A", active=True),
            factories.ProductFactory(name="B", active=True),
            factories.ProductFactory(name="C", active=True),
        ]

        orders = factories.OrderFactory.create_batch(3)

        factories.OrderLineFactory.create_batch(
            2, order=orders[0], product=products[0]  # A: 2
        )
        factories.OrderLineFactory.create_batch(
            2, order=orders[0], product=products[1]  # B: 2
        )
        factories.OrderLineFactory.create_batch(
            2, order=orders[1], product=products[0]  # A: 2+2
        )
        factories.OrderLineFactory.create_batch(
            2, order=orders[1], product=products[2]  # C: 2
        )
        factories.OrderLineFactory.create_batch(
            2, order=orders[2], product=products[0]  # A: 2+2+2
        )
        factories.OrderLineFactory.create_batch(
            1, order=orders[2], product=products[1]  # B: 2+1
        )

        user_one = models.User.objects.create_superuser(
            "user_one", "whatislove"
        )
        self.client.force_login(user_one)

        response = self.client.post(
            reverse("admin:most_bought_products"),
            { "period": "90" },
        )
        self.assertEqual(response.status_code, 200)

        data = dict(zip(
            response.context["labels"],
            response.context["values"],
        ))

        self.assertEqual(data, { "B": 3, "C": 2, "A": 6 })

    def test_invoice_renders_exactly_as_expected(self):
        products = [
            factories.ProductFactory(name="A", active=True, price=Decimal("1.00")),
            factories.ProductFactory(name="B", active=True, price=Decimal("5.00")),
        ]

        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = datetime(
                2019, 2, 2, 12, 00, 00
            )

            order = factories.OrderFactory(
                id=12,
                billing_name="John Smith",
                billing_address1="add1",
                billing_address2="add2",
                billing_zip_code="zip",
                billing_city="London",
                billing_country="UK",
            )

            factories.OrderLineFactory.create_batch(
                2, order=order, product=products[0]  # A: 2
            )
            factories.OrderLineFactory.create_batch(
                2, order=order, product=products[1]  # B: 2
            )

            user_two = models.User.objects \
                .create_superuser("user_two", "thatsgreat")
            self.client.force_login(user_two)

            # ********************-----**********************
            # ***************** print HTML ******************
            # ********************-----**********************

            response = self.client.get(
                reverse(
                    "admin:invoice", kwargs={ "order_id": order.id }
                )
            )

            self.assertEqual(response.status_code, 200)
            content = response.content.decode("utf8")

            with open("main/fixtures/invoice_test_order.html", "r") as fixture:
                expected_content = fixture.read()

            self.assertEqual(content, expected_content)

            # ********************-----**********************
            # ***************** print PDF ******************
            # ********************-----**********************

            response = self.client.get(
                reverse(
                    "admin:invoice", kwargs={ "order_id": order.id }
                ),
                data={ "format": "pdf" }
            )

            self.assertEqual(response.status_code, 200)
            content = response.content

            with open("main/fixtures/invoice_test_order.pdf", "rb") as fixture:
                expected_content = fixture.read()

            self.assertEqual(content, expected_content)
