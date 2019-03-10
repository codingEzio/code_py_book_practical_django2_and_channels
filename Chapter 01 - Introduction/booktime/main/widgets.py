from django.forms.widgets import Widget


class PlusMinusNumberInput(Widget):
    """
    What is 'widget' anyway?
        A widget is Django’s representation of an HTML input element.
        Thus, it's PART of the "form fields" (like `IntegerField`). Yep, it's smaller.

    A better widget to manage changes to <product quantities>.
        The one we'll modify is also an "input" widget, that's why we import the `Widget`.
    """

    template_name = "widgets/plusminusnumber.html"

    class Media:
        """
        This part will also be translated as HTML code,
        e.g.
            <link   type="text/css"        href=".." >
            <script type="text/javascript" src =".." ></script>
        """

        css = {
            "all": ("css/plusminusnumber.css",)
        }
        js = (
            "js/plusminusnumber.js",
        )