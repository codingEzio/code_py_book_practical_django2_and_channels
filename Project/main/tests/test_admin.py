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
            2, order=orders[0], product=products[0]     # A: 2
        )
        factories.OrderLineFactory.create_batch(
            2, order=orders[0], product=products[1]     # B: 2
        )
        factories.OrderLineFactory.create_batch(
            2, order=orders[1], product=products[0]     # A: 2+2
        )
        factories.OrderLineFactory.create_batch(
            2, order=orders[1], product=products[2]     # C: 2
        )
        factories.OrderLineFactory.create_batch(
            2, order=orders[2], product=products[0]     # A: 2+2+2
        )
        factories.OrderLineFactory.create_batch(
            1, order=orders[2], product=products[1]     # B: 2+1
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
