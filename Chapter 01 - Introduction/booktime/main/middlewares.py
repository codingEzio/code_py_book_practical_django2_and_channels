from . import models


def basket_middleware(get_response):
    def middleware(request):
        """
        It basically does this:
        -- 1. If there's a basket before (in session/cookie),
              get it and assign it to the current page (request.basket).
        -- 2. The 'request.basket' will be eventually be used
              by the methods in 'views.py' (which is the 'add_to_basket')
        """

        if 'basket_id' in request.session:
            basket_id = request.session["basket_id"]
            basket = models.Basket.objects.get(id=basket_id)

            request.basket = basket
        else:
            request.basket = None

        response = get_response(request)

        return response

    return middleware