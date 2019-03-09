
### Creating the *Basket* functionality
- Here's how we do
    1. *models*

        ```python
        class Basket(models.Model):
             = ..
             = ..
             = ..
             = ..
             = ..

        class BasketLine(models.Model):
             = ..
             = ..
             = ..
        ```

    2. *migrations*

        ```bash
        ./manage.py makemigrations
        ./manage.py migrate
        ```

    3. *middlewares* 

        ```python
        """
        A brief intro for 'middleware'
        -- It's a function that wraps and offer additional functionalities to view.
        -- It could modify requests as they come in & and response as they come out.
        """

        # Go check the code for more details.

        # It basically does this:
        # -- 1. If there's a basket before (in session/cookie),
        #       get it and assign it to the current page (request.basket).
        # -- 2. The 'request.basket' will be eventually be used
        #       by the methods in 'views.py' (which is the 'add_to_basket')
        ```

    4. *settings* 

        ```python
        """ settings.py """
        
        MIDDLEWARE = [
            .. , 
            .. ,
            "main.middlewares.basket_middleware" ,
        ]
        ```

    4. *templates*

        ```html
        <!-- 
            Add this before the "{% block content %}" part in <base.html>
        -->

        {% if request.basket %}
	        <div>
	        	{{ request.basket.count }}
	        	items in basket
	        </div>
        {% endif %}


        <!-- 
            Replace the original <a href=..> in <product_detail.html>
        -->

        <a href="{% url 'main:add_to_basket' %}?product_id={{ object.id }}">
                Add to basket
        </a>

        ```

    5. *views*

        ```python
        # Go check the code, detailed notes out there!
        ```

    6. *urls*

        ```python
        path(
            "add_to_basket/",
            views.add_to_basket, 
            name="add_to_basket"
        )
        ```

    7. *tests*

        ```python
        """ Location :: main/tests/test_views.py :: TestPage """

        # Two things basically
        # 1. Does the products being correctly added to the cart
        # 2. Does the amount of product in basket will be increased


        """ How to test it, exactly? """
        # 1. Go to the product page, like `localhost:8000/product/siddhartha/`
        # 2. Click the 'add-to-basket' button (you could buy it multiple times though).
        # 3. After you've made up ur mind, the number would be displayed at the top.
        ```
