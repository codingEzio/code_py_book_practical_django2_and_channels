from decimal import Decimal

from django.test import TestCase

from main import models
from main import factories


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

        factories.ProductFactory.create_batch(2, active=True)
        factories.ProductFactory(active=False)

        # The test objects here are only two "active" objs
        # so that's why the 2nd param of `assertEqual` is "2".
        self.assertEqual(len(models.Product.objects.active()), 2)

    def test_create_order_works(self):
        """
        """

        prod_one = factories.ProductFactory()
        prod_two = factories.ProductFactory()
        user_one = factories.UserFactory()
        billing = factories.AddressFactory(user=user_one)
        shipping = factories.AddressFactory(user=user_one)

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
        self.assertEquals(order.billing_address1, billing.address1)
        self.assertEquals(order.shipping_address1, shipping.address1)

        # two products while checking out
        self.assertEquals(order.lines.all().count(), 2)

        # same as the prev line, just break it down as a list
        lines = order.lines.all()
        self.assertEquals(lines[0].product, prod_one)
        self.assertEquals(lines[1].product, prod_two)