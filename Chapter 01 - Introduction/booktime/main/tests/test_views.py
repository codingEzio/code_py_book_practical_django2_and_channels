from django.test import TestCase
from django.urls import reverse

from main import forms


class TestPage(TestCase):
    def test_home_page_works(self):
        """
        Frankly, these comments aren't necessary for me.
        But.. Just in case I forgot this, I'll put some notes in here.

        `assertContains`    Does the page contains strings like 'BookTime'?
        `reverse("home")`   The "home" is the `name` attr in the `urlpatterns`.
        """

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "BookTime")

    def test_about_page_works(self):
        response = self.client.get(reverse("about_us"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about_us.html")
        self.assertContains(response, "BookTime")

    def test_contact_us_page_works(self):
        response = self.client.get(reverse("contact_us"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact_form.html")
        self.assertContains(response, "BookTime")
        self.assertIsInstance(
            response.context["form"], forms.ContactForm
        )