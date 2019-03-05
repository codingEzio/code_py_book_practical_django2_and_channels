import logging

from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib import messages

from main import forms, models

logger = logging.getLogger(__name__)


class ProductListView(ListView):
    template_name = "main/product_list.html"
    paginate_by = 4

    def get_queryset(self):
        """
        Ah, the two `tag`s here are NOT the same.
        """

        tag = self.kwargs["tag"]
        self.tag = None

        if tag != "all":
            self.tag = get_object_or_404(models.ProductTag, slug=tag)

        if self.tag:
            products = models.Product.objects.active().filter(tags=self.tag)
        else:
            products = models.Product.objects.active()

        return products.order_by("name")


class ContactUsView(FormView):
    """
    What if you wanna write this in 'Function-based' way?

        def contact_us(request):
            if request.method == "POST":
                form = forms.ContactForm(request.POST)

                if form.is_valid():
                    form.send_mail()
                    return HttpResponseRedirect("/")
            else:
                form = forms.ContactForm()

            return render(request, "contact_form.html", {"form": form})

    Okay.. Whatever :P
    """

    template_name = "contact_form.html"
    form_class = forms.ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class SignupView(FormView):
    """
    This is actually two parts.
    -- One for 'registration' page
    -- One for 'sending email' feature

    The `FormView` is quite special here.
    1. It's one of the `ModelView` type.
    2. The <data submitted> can be automatically stored in a model.

    According to the author,
        the `authenticate` will ALWAYS work in the same way
        even if you're using some other auth methods (DB-based, LDAP etc.)

    And the `messages`
        it was used to "flash" a message to users (after doing/finished sth).

        e.g.
            https://www.w3schools.com/bootstrap/bootstrap_alerts.asp
            https://codepen.io/danrosenthal/pen/BWyORL?html-preprocessor=slim (complex)
    """

    template_name = "signup.html"
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()

        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")

        logger.info(
            "New signup for email=%s through SignupView", email
        )

        user = authenticate(email=email, password=raw_password)
        login(self.request, user)

        form.send_mail()

        messages.info(
            self.request, "You signed up successfully :D"
        )

        return response