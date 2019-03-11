### A better *widget* 
- which is used for changing **quantity** of products in the basket.
- Here's how we do it
    
    1. *widgets*

        ```python
        # There're related FOUR files
        # || widgets.py              # Specify the modified template ( CSS, JS included )
        # || plusminusnumber.html    # Basic 'one-input & two-btns'  ( behavior changes, though )
        # || plusminusnumber.css     # Replace the default with our own buttons
        # || plusminusnumber.js      # Functionalities for buttons (plus|minus) ( & related input )
        
        # Go check the code, XD!
        # The 'widgets.py' is just like a "form", but smaller, abstractly.
        ```
       
    2. *forms*

        ```python
        BasketLineFormSet = inlineformset_factory(
            .. ,
            .. ,
            .. ,
            .. ,
            widgets={ "quantity" : widgets.PlusMinusNumberInput() }    # our customized 'input'
        )
        ```
        
    3. *templates*

        ```html
        <!-- 
            PROJECT/main/templates :: base.html
        -->
        
        {% block js %}
        {% endblock js %}
        
        
        <!-- 
            PROJECT/main/templates :: wigets/plusminusnumber.html
        -->
        
        {% block js %}
    	      {% if formset %}
    		        {{ formset.media }}
	          {% endif %}
        {% endblock js %}
        ```
        
### *Orders* & *Checkouts* 
- Still, the 1st thing to do is to lay the *foundations*, aka. ***models***.
    - Similar names compare to ```Basket```, namely, ```Order``` & ```OrderLine```.
    - Oh, do remember to run this command after writing the models

        ```bash
        ./manage.py makemigrations
        ./manage.py migrate
        ```
        
- The *Foundations*
    
    1. *exceptions*
        
        ```python
        # Nothing fancy ( lives in 'main/exceptions.py' )
        
        class BasketException(Exception):
            pass
        ```
    
    2. *models* :: NEW
    
        ```python
        class Order    (..):
            # user
            # status
            # billing  info
            # shipping info
            # date     created|updated 
            
        class OrderLine(..):
            # order
            # status
            # product
        ```

    3. *models* :: NEW method for OLD model
    
        ```python
        class Basket(..):
            ..
            ..
            
            def create_order( .. , .. , .. ):
                
        ```
    
    4. *tests*

        ```python
        # Procedures
        # 1. Setup the base: 1-user, 2-prod, address-billing, address-shipping
        # 2. Add products to basket: xxx's-basket <= adding-two-prod-to-it
        # 3. Testing logs which is being setup in the 'models.py'
        # 4. Testing correct-user | correct-addresses
        # 5. Testing products in the basket | orders
        ```