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
    - Oh, do remember to ***run this command after writing the models***

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

- The other part: *display billing|shipping addresses*

    1. *forms*

        ```python
        class AddressSelectionForm(forms.Form):
            """
            It's still a part of the template, dedicated to `<form>` only.
            """

            billing_address  = forms.ModelChoiceField(queryset=None)
            shipping_address = forms.ModelChoiceField(queryset=None)

            def __init__(self, user, ..):
                super().__init__(..)

                queryset = .. filter(user=user)

                ..
                ..
        ```

    2. *views*

        ```python
        # 1. Extract the user then inserting it to the response.
        # 2. Create  order with the data provided by `AddressSelectionForm`.
        # 3. Template base | success_page 
        ```

    3. *templates* ADD

        ```html
        <!-- main/templates :: address_select.html -->

        <!-- 
            1. The address choice field was done by `forms.py`
            2. A 'submit' button
            3. A 'add a new one(addr)' link 
        -->
        ```

    4. *templates* ADD

        ```html
        <!-- main/templates :: order_done.html -->

        <!-- 
            The 'success' page (nothing fancy).
        -->
        ```

    5. *templates* UPDATE

        ```html
        <!-- main/templates :: basket.html -->
        
        <!-- 
            If logged in 
                display the 'Place order' (which points to "address_select")

            If not logged in
                display the links: "Signup", "Login" (with `next` params)
        -->
        ```

    6. *urls*

        ```python    
        path(
            "order/done/",
            TemplateView.as_view(template_name="order_done.html"),name="checkout_done"
        ),

        path(
            "order/address_select/",
            views.AddressSelectionView.as_view(),
            name="address_select"
        ),
        ```

    7. *testing* <small>( usage )</small>

        ```bash
        # Havn't try it yet.
        ```

### Hey, just so you know
- There were two missing pieces in the most-recent commit messages.
    1. Display *Basket* & *Order* info at the *admin* site. 
    2. One more ```imageswitch``` function inside the **product_detail.html** page.
- Issues
    - The *imageswitch* function seems stopped working.
        - SHOULD  : *click one of them to see its bigger picture*
        - CURRENT : *display both the small/big pictures*
- Test for the newly added *functionality* (huh)
    1. Base

        ```bash
        pipenv install selenium                                 # your env
        https://chrome.google.com                               # /Applications/
        https://chromedriver.storage.googleapis.com/index.html  # /usr/local/bin/

        # Test files
        cp -rf OFFICIAL_REPO/main/fixtures/cb YOUR_REPO/main/fixtures/fixtures/
        ```
    
    2. Code

        ```python
        # Get
        # Find
        # Click
        # Compare
        ```

---------


### Build tools for *static files*
- More clearly, we'll install these stuff
    1. Bundler
    2. Loader
    3. Framework
- Base

    ```bash
    npm install -y      # same level as 'manage.py'

    npm install react react-dom         --save
    npm install webpack webpack-cli     --savedev
    npm install webpack-bundle-tracker  --savedev

    pipenv install django-webpack-loader

    
    # Just so you know, after the installation,
    #   there's some modification in the `package.json`.
    ```

- Config

    1. *Webpack* config

        ```bash
        # WHERE     same level as 'manage.py'
        # NAME      'webpack.config.js'
        ```

    2. *Webpack* config :: **Django**

        ```python
        # PROJECT/booktime/settings.py 

        # 1. INSTALLED_APPS     ..
        # 2. WEBPACK_LOADER     ..
        ```

    3. Decouple the *CSS* & *JS* from the templates

        ```javascript
        /*
        ORIGINAL        PROJECT/main/templates/main/product_detail.html
        DESTINATION     PROJECT/frontend/imageswitcher.js

        Note
            Just go check the code. Too damn hard to make it work :P
            
            After you've done that, 
            run `npm run build` at PROJECT level.
        */ 
        ```

- Issues
    1. Bunch of errors out there, ah..
    2. IT JUST DOESN'T WORK <small>( switch-image )</small>
    3. This part is such a mess that I'll just *skip* this part without too much details :(