import logging

from django import forms
from django.core.mail import send_mail


from django.contrib.auth.forms import (
    UserCreationForm as OurUserCreationForm
)
from django.contrib.auth.forms import UsernameField

from . import models


logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=100)
    message = forms.CharField(
        max_length=600, widget=forms.Textarea
    )

    def send_mail(self):
        logger.info("Sending email to customr service ..")

        message = "From: {0}\n{1}".format(
            self.cleaned_data["name"],
            self.cleaned_data["message"]    
        )

        send_mail(
            "Site message",
            message,
            "site@booktime.domain",
            ["customerservice@booktime.domain"],
            fail_silently=False,
        )


class UserCreationForm(OurUserCreationForm):
    class Meta(OurUserCreationForm.Meta):
        """
        A little modification due to changes in 'model' & 'admin' site.

        Specifically, I'm talkin' about the `fields` & `field_classes`.
        Since we've change the 'name+pwd' to 'mail+pwd'
            We'll need to override the default one ( aka `UserCreationForm` )

        By the way,
            the `field_classes` is just <use> the `fields`
            Those two are <together> :D
        """

        model = models.User
        fields = ("email", )
        field_classes = {"email": UsernameField}

    def send_mail(self):
        """
        Cuz you <need> to send <registration info>.
        That means you <need> this function (not the other reasons, apparently).
        """

        logger.info(
            "Sending signup email for email=%s",
            self.cleaned_data["email"],
        )
        message = "Welcome{}".format(self.cleaned_data["email"])

        # TODO as a marker (the 'email' might need to change!)
        send_mail(
            "Welcome to BookTime",
            message,
            "admin@example.com",
            [self.cleaned_data["email"]],
            fail_silently=True,
        )