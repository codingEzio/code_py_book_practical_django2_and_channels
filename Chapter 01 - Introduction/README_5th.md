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

    5. *templates*

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
    
    6. *views*
    
     ```python
        # Go check the code, detailed notes out there!
     ```
    
    7. *urls*
    
     ```python
        path(
            "add_to_basket/",
            views.add_to_basket, 
            name="add_to_basket"
        )
     ```
    
    8. *tests*
    
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

### Manage *basket* **view**

- What we need 
  - Features
    - A page to **modify the content** of the *basket*
      1. *change quantities* 
      2. *delete lines* from the basket.
  - Technique
    - The *formsets*, which is a **multiple forms on the same page**.
- Implementing it 
  1. *forms*

     ```python
      """ File :: main/forms.py"""
     
      BasketLineFormSet = inlineformset_factory(
          models.Basket,
          models.BasketLine,
     
          # The quantity will surely be displayed.
          # There's also a 'delete' button provided by `inlineformset_factory`.
          fields=("quantity",),
          extra=0,
      )
     ```

  2. *views*

     ```python
      # It mainly does these things
      # -- What to render (no-basket,  have-basket-but-zero, GET, POST)
      # -- Validate
      # -- Save data to database
     ```

  3. *templates*

     ```html
      <!-- Display the formsets & the 'submit' button. -->
     
      ...
     
      <form method="POST"> {% csrf_token %}
          {% for form in formset %}
              <p>
                  {{ form.instance.product.name }}
                  {{ form }}
              </p>
          {% endfor %}
     
          <button type="submit" class="btn btn-primary">
              Update basket
          </button>
      </form>
     
      ...
     ```

  4. *urls*

     ```python
     path(
         "basket/",
         views.manage_basket, 
         name="basket"
     )
     ```

  5. usage
  
      ```bash
      # Firstly, adding some products.
      #   e.g. http://localhost:8000/product/siddhartha/
     
      # After you've satisfied (XD)
      #   access this page: http://localhost:8000/basket/ 
     
      # You could do these 
      #   1. Update the quantity of products
      #   2. Delete products from the basket :D
     ```

---

### Foreword for the next section

- Do remember there's a big difference between *Taobao* & *Ebay* <small>( and any other non-local sites )</small>
    - You *cannot* buy stuff without logging in, which is, the bloody *Taobao*.
    - But another version of it, aka. *AliExpress*, might actually able to do this.
- I've done some *searching* in order to find what sites can *do* this.
    - Here's a dead simple comparison
        1. *Ebay* <small>( without logging in: *add-to-cart*, *checkout* )</small>
        2. *Amazon* <small>( without logging in: *add-to-cart* )</small>
        3. *Taobao* <small>( without logging in: **N/A** )</small>

### A brief *review* for the code we've written
- Apparently, what I'm talking about is the *basket* functionalities,
    - which is, now that you can 
        - *put products into the basket* 
        - *edit the amount of products in the basket*.
- There's still some features we havn't implemented yet,
    - For example, **merging the baskets after user logged in**.
    - That means you could add stuff to basket even if you're just a *anonymous* user.
- You should **clean up** the ```basket```, ```basketline``` table **each time** before you start testing.

### What needs to be written
1. *signals*

    ```python
    # Go check the code (main/signals.py) anyway.
    # I havn't cleaned this up, just a bunch of comments won't help much.
    ```

2. *tests*
    - Manually testing

        ```bash
        # First make sure the database is clear
        # which is, the `main_basket` & `main_baskline` must be blank.
        
        # Then make sure you've logged off ( => localhost:8000/admin/ )
        # Now you can start buying stuff, URLs could be like this
        #   http://localhost:8000/products/the-cathedral-and-the-bazaar/
        #   http://localhost:8000/products/backgammon-for-dummies/
        #   http://localhost:8000/products/siddhartha/
        
        # After doing the purchase, login with ur account
        # then go check the basket: http://localhost:8000/basket/
        ```
    
    - The code <small>( structure )</small>

        ```python
        # 1. One user, two products
        # 2. Buy stuff, total num is three
        # 3. Log in, check { auth, auth_success_or_not }
        # 4. Check the number of product in the basket ( merged => three products )
        ```

---
