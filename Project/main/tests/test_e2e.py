from decimal import Decimal

from django.test import tag
from django.urls import reverse
from django.core.files.images import ImageFile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from main import models

@tag("e2e")
class FrontendTests(StaticLiveServerTestCase):
    """
    If using the code in the books
        >> from selenium.webdriver.firefox.webdriver import WebDriver
        >> cls.selenium = WebDriver()

        You might encounter this:
            selenium.common.exceptions.SessionNotCreatedException:
            ↑ Message: Unable to find a matching set of capabilities

    I myself choose to use the 'chromedriver' (solved the issue accidentally..)
        The code here is a little different,
        but I think it's even more intuitive than before :)

        Download here
            https://chromedriver.storage.googleapis.com/index.html
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
        cls.selenium.implicitly_wait(20)

    @classmethod
    def tearDownClass(cls):

        # If you wanna see the result (gen_ed thumbnails)
        # just commenting this line to make it stay that way.
        cls.selenium.quit()

        super().tearDownClass()

    def test_product_page_switches_images_correctly(self):
        """
        Well.. the tests would pass (& working perfectly fine).

        Ah.. the weird thing is
        it won't work if you access it normally (two pics only).
        """

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
