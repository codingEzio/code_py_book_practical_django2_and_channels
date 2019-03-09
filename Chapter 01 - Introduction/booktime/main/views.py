import logging

from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.views.generic.list import ListView
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)

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


ADDRESS_FIELDS = [
    "name",
    "address1",
    "address2",
    "zip_code",
    "city",
    "country",
]


class AddressListView(LoginRequiredMixin, ListView):
    model = models.Address

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = models.Address
    fields = ADDRESS_FIELDS
    success_url = reverse_lazy("main:address_list")

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.user = self.request.user
        obj.save()

        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Address
    fields = ADDRESS_FIELDS
    success_url = reverse_lazy("main:address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Address
    success_url = reverse_lazy("main:address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


def add_to_basket(request):
    """
    The <middlewares> we've written helps us to get the "basket in session|cookie".

    Some results (might be bugs, or not)
    -- 1. You could buy the same product multiple times.
    -- 2. You could buy products without logging in (huh?).
    -- 3. ..
    """

    # Get ONE product at a time (every time you clicked the 'add_to_basket')
    product = get_object_or_404(
        models.Product, pk=request.GET.get("product_id")
    )

    # Whether there is BASKET in the session storage
    # Yep -> Okay
    # Nah -> None
    basket = request.basket

    # If the basket is NULL
    if not request.basket:

        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        # Create a basket with current user (or None)
        #   That means <You CAN "add products to basket" without logging in!>
        basket = models.Basket.objects.create(user=user)

        # Create a session storage in browser
        request.session["basket_id"] = basket.id

    # Add the 'product' to the 'basket'
    #   and the `created` arg is a boolean value (succeeded or not)
    basketline, created = models.BasketLine.objects.get_or_create(
        basket=basket, product=product
    )

    # True  ->  Equals to 'buy the product first time'
    # False ->
    #   Cuz the above (basket, product) is the same,
    #   that means you can't create the objects again (which products 'False').
    #   ---------- Ah, the logic is quite NOT intuitive, hell no! ----------
    #   The 'False' resulted in you're NOT the first time to buy it
    #   thus the quantity of the product in the basket should be increased.
    if not created:
        basketline.quantity += 1
        basketline.save()

    # Pitfall
    #   Mixed 'args=(product.slug,)' with 'args=(product.slug)'  ( the ',' )
    #   It'll be a sole string instead of a tuple (it should be a tuple by the way).
    # The mechanics
    #   since the {'buy the prod 1st time', 'increase the quantity'}
    #   has been implemented by code above, the only thing for `return`
    #   statement is to redirect the user to the respective product's page!
    return HttpResponseRedirect(
        reverse("main:product", args=(product.slug,))
    )


def manage_basket(request):
    """
    """

    # The user doesn't have a basket yet (just browsing)
    if not request.basket:
        return render(request, "basket.html", { "formset": None })

    if request.method == "POST":

        # Post actions (deletion)
        formset = forms.BasketLineFormSet(
            request.POST, instance=request.basket
        )

        if formset.is_valid():
            formset.save()
    else:

        # Method 'GET' (display the form only)
        formset = forms.BasketLineFormSet(
            instance=request.basket
        )

    # The user do has a basket, but with its amount of product is zero ?!
    if request.basket.is_empty():
        return render(request, "basket.html", { "formset": None })

    return render(request, "basket.html", { "formset": formset })