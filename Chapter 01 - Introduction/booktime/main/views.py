from django.views.generic.edit import FormView

from main import forms


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
