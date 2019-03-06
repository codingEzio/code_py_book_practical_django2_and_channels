import logging

from django import forms
from django.core.mail import send_mail


from django.contrib.auth.forms import (
    UserCreationForm as OurUserCreationForm
)
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import authenticate
from django.contrib import messages

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


class AuthenticationForm(forms.Form):
    """
    The page being redirected to is define as an const.
    In 'settings.py'
        append => LOGIN_REDIRECT_URL = "/"
    """

    email = forms.EmailField()
    password = forms.CharField(
        strip=False, widget=forms.PasswordInput
    )

    def __init__(self, request=None, *args, **kwargs):
        """
        Since we're doing "auth" solely inside this `forms.py`.
        We'll need to 'get' the request info (just like 'views' did).

        Just so you know, the "forms" and "views" has some similarities.
        I'll elaborate this in the 'README_NUM' notes (upper level -> projet).
        """

        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:

            # Auth with [email+password]
            self.user = authenticate(
                self.request, email=email, password=password
            )

            # Auth failed
            if self.user is None:
                messages.warning(
                    self.request, "Invalid email/password combination."
                )
                raise forms.ValidationError(
                    "Invalid email/password combination."
                )

            # What if you don't input anything?
            # => You're actually being stop at the very first (by HTML).

            # The code will execute to here
            # if everything is going great (success => terminal log info).
            logger.info(
                "Authentication successful for email=%s", email
            )
            messages.success(
                self.request, "Authentication successful!"
            )

        return self.cleaned_data

    def get_user(self):
        return self.user