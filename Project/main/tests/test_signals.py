from decimal import Decimal

from django.test import TestCase
from django.core.files.images import ImageFile

from main import models


class TestSignals(TestCase):
    """
    Since I need to make sure everything is WORKING,
    I'll just using the examples from the book, I might change it later on.
    """

    def test_thumbnails_are_generated_on_save(self):
        """
        Overview
        1. product init inst & save
        2. product image (original)
        3. product image (thumbnail)

        The 'signals.py' lies between "models" & "views",
        you don't actually can see it 
        """


        product = models.Product(
            name="The Cathedral and the bazaar", price=Decimal("3.00")
        )

        product.save()

        with open("main/fixtures/the-cathedral-the-bazaar.jpg", "rb") as fi:
            image = models.ProductImage(
                product=product, image=ImageFile(fi, name="tctb.jpg")
            )

            with self.assertLogs("main", level="INFO") as cm:
                image.save()

        self.assertGreaterEqual(len(cm.output), 1)
        image.refresh_from_db()

        with open("main/fixtures/the-cathedral-the-bazaar.thumb.jpg", "rb") as fi:
            expected_content = fi.read()
            assert image.thumbnail.read() == expected_content

        image.thumbnail.delete(save=False)
        image.image.delete(save=False)
