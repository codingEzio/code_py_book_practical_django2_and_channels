from decimal import Decimal

from django.test import tag
from django.urls import reverse
from django.core.files.images import ImageFile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium import webdriver

from main import models


@tag("e2e")
class FrontendTests(StaticLiveServerTestCase):
    """
    There're always an error
        selenium.common.exceptions.SessionNotCreatedException:
        Message: Unable to find a matching set of capabilities
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = WebDriver()
        # cls.selenium = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()

        super().tearDownClass()

    def test_product_page_switches_images_correctly(self):
        product = models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )

        for fname in ["cb1.jpg", "cb2.jpg", "cb3.jpg"]:
            with open("main/fixtures/cb/%s" % fname, "rb") as fi:
                image = models.ProductImage(
                    product=product,
                    image=ImageFile(fi, name=fname),
                )

                image.save()

        self.selenium.get(
            "%s%s" % (
                self.live_server_url,
                reverse(
                    "main:product",
                    kwargs={"slug": "cathedral-bazaar"},
                )
            )
        )

        current_image = self.selenium \
            .find_element_by_css_selector(".current-image > img:nth-child(1)") \
            .get_attribute("src")

        self.selenium \
            .find_element_by_css_selector("div.image:nth-child(3) > img:nth-child(1)") \
            .click()

        new_image = self.selenium \
            .find_element_by_css_selector(".current-image > img:nth-child(1)") \
            .get_attribute("src")

        self.assertNotEqual(current_image, new_image)
