from decimal import Decimal

from django.test import TestCase

from main import models


class TestModel(TestCase):
    def test_active_manager_works(self):
        """
        The "manager" itself lives in the 'models.py'

        Example code
        >>> class ActiveManager(models.Manager):
        >>>     def active(self):
        >>>         return self.filter(active=True)

        >>> class Product(models.Model):
        >>>     ...
        >>>     objects = ActiveManager()
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
        # so that's why the 2nd param of `assertEqual` is "2"
        self.assertEqual(len(models.Product.objects.active()), 2)
