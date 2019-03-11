from decimal import Decimal

from django.test import TestCase

from main import models


class TestModel(TestCase):
    def test_active_manager_works(self):
        """
        The "manager" itself lives in the 'models.py'

        Example code
        >> class ActiveManager(models.Manager):
        >>     def active(self):
        >>         return self.filter(active=True)

        >> class Product(models.Model):
        >>     ...
        >>     objects = ActiveManager()
        """

        models.Product.objects.create(
            name="The cathedral and the bazaar", price=Decimal("10.00")
        )
        models.Product.objects.create(
            name="Price and Prejudice", price=Decimal("2.00")
        )
        models.Product.objects.create(
            name="A Tale of Two Cities", price=Decimal("2.00"), active=False
        )

        # The test objects here are only two "active" objs
        # so that's why the 2nd param of `assertEqual` is "2".
        self.assertEqual(len(models.Product.objects.active()), 2)

    def test_create_order_works(self):
        """
        """

        prod_one = models.Product.objects.create(
            name="Product One",
            price=Decimal("1.00"),
        )
        prod_two = models.Product.objects.create(
            name="Product Two",
            price=Decimal("2.00"),
        )
        user_one = models.User.objects.create_user(
            "user_one", "thisisfun"
        )
        billing = models.Address.objects.create(
            user=user_one,
            name="Jamie Lannister",
            address1="Westworld",
            city="London",
            country="uk",
        )
        shipping = models.Address.objects.create(
            user=user_one,
            name="Jamie Lannister",
            address1="Westworld",
            city="London",
            country="uk",
        )

        basket = models.Basket.objects.create(user=user_one)

        models.BasketLine.objects.create(
            basket=basket, product=prod_one
        )
        models.BasketLine.objects.create(
            basket=basket, product=prod_two
        )

        with self.assertLogs("main.models", level="INFO") as cm:
            order = basket.create_order(billing, shipping)

        self.assertGreaterEqual(len(cm.output), 1)

        order.refresh_from_db()

        # user_one's order
        self.assertEquals(order.user, user_one)

        # correct billing|shipping addresses
        self.assertEquals(order.billing_address1, "Westworld")
        self.assertEquals(order.shipping_address1, "Westworld")

        # two products while checking out
        self.assertEquals(order.lines.all().count(), 2)

        # same as the prev line, just break it down as a list
        lines = order.lines.all()
        self.assertEquals(lines[0].product, prod_one)
        self.assertEquals(lines[1].product, prod_two)
