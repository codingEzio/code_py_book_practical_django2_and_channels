from django.test import TestCase


class TestPage(TestCase):
    def test_home_page_works(self):
        """
        Frankly, these comments aren't necessary for me.
        But.. Just in case I forgot this, I'll put some notes in here.

        `assertContains`    Does the page contains strings like 'BookTime'?
        """

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "BookTime")

    def test_about_page_works(self):
        response = self.client.get("/about-us/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about_us.html")
        self.assertContains(response, "BookTime")
