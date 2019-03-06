
### Page :: *Product List*
- What needs to be written
    1. *views*

        ```python
        # For the sake of simplicity, I won't show all the code here.

        # Specify
        # -- templates location
        # -- paging num by your need 

        # Also, you could specific tags, or not.
        # the params was given while you're accessing the URL.
        if self.tag:
            .. filter(tags=self.tag)
        else:
            .. 
        ```

    2. *urls*

        ```python
        # Just to make sure the routes will work
        app_name = "main"

        path(
            "products/<slug:tag>/",
            ..  # view func
            ..  # name used in templates
        )
        ```

    3. *templates*

        ```html
        <!-- 
        Still, for the sake of brevity, I'll only show a little bit of it.

        The code down below is kinda hard-to-understand (for me)
        
            `page_obj`          related to `paginate_by` in our view
            `main:products`     APP_NAME:URLPATTERN_NAME (err in book)
        -->

        {% for product in page_obj %}
            ...

            {{ product.name }}

            {% url 'main:product' product.slug %}

            ...
        {% endfor %}
        ```

- Testing
    - Usage

        ```bash
        # Preq
        # 1. The 'slug' cannot be null for the related tag.
        # 2. What you've passed is "the slug" (slugified tag).

        open http://localhost:8000/products/all/
        open http://localhost:8000/products/open-source/
        ```
    
    - Tests

        ```python    
        # PROJECT/main/tests :: TestPage
        # -- test_products_page_returns_active
        # -- test_products_page_filters_by_tags_and_active

        # Nothing fancy, just these steps:
        # 1. create objects
        # 2. `client.get` the page (like a real user)
        # 3. do asserting (e.g. `assertEqual`, `assertContains`)
        ```
    
- Oh, one more thing!
    - Since I've added the ```app_name = 'main'``` to ```urls.py```
    - There's some changes you need to made (in tests)

        ```python
        self.client.get(reverse(     "contact_us"))    # OLD
        self.client.get(reverse("main:contact_us"))    # NEW
        ```


### Page :: *Single Product*
- What needs to be written
    1. *templates*

        ```html
        <!-- 
        Ah, the template itself is quite simple.
        Just with more "template filters" this time.

        Something like this
            object.description|linebreaks
            object.in_stock|yesno|capfirst
            object.date_updated|date:"F Y"
            object.tags.all|join:","|default:"No tags availabel :("
        -->

        <!-- 
        Oh, also the book got some errors (or not)
            {% url 'add_to_basket' %}?product_id={{ object.id }}
        
        Since we (and the book) havn't impl it yet,
        you need to change the value of `href` to "#" (at least temporarily).
        -->
        <a href="#">
		    Add to basket
	    </a>
        ```
    
    2. *urls*

        ```python
        from django.views.generic.detail import DetailView
        from main import models

        path(
            "product/<slug:slug>/", 
            DetailView.as_view(model=models.Product),   # How convinient!
            name="product"                              # used in templates
        )
        ```

- Testing <small>( *usage* as well )</small>
    
    ```bash
    # Ah, the name could be different from yours, though.
    
    open http://localhost:8000/product/siddhartha/
    open http://localhost:8000/product/backgammon-for-dummies/
    open http://localhost:8000/product/the-cathedral-and-the-bazaar/
    ```


-------------

### Customizing ```User``` *model*
- What needs to be <small>(re)</small>written
    1. *models*

        ```python
        # For the sake of simplicity, I'll omit most of the details.

        class UserManager(BaseUserManager):
            def _create_user(..):
                """ This is a helper method for the other methods
                """

                ..
                .. self.model  (email=email, ..)
                .. set_password(password)
                ..

            def create_user     (..):
                ..
                .. setdefault("is_staff", False)
                .. setdefault("is_admin", False)
                ..

            def create_superuser(..):
                .. setdefault("is_staff", False)
                .. setdefault("is_superuser", True)
                ..


        class User(AbstractUser):    
            username = None
            email    = models.EmailField(..)

            USERNAME_FIELD  = ..    # mostly, `CharField` or `EmailField` (or both?!)
            REQUIRED_FIELDS = ..    # specifically, "required" when creating superuser

            objects = UserManager() # using the "modified" manager :P
        ```
    
    2. *admin*
        ```python
        from django.contrib.auth.admin import UserAdmin as OrigUserAdmin
        
        @admin.register(models.User)
        class UserAdmin(OrigUserAdmin):
            """
            It's no different in comparing with the other `field`s in other models.

            What does `fieldsets` (here) for?
                =>  Define the fields that'll be displayed on the 'create user' page.
            What does `add_fieldsets` for?
                =>  Define the fields that'll be displayed on the 'new user' page.
            """

            fieldsets       = ( .. )
            add_fieldsets   = ( .. )

            list_display    = ( .. )
            search_fields   = ( .. )

            ordering        = ( .. )
        ```
    3. *settings*

        ```python
        # append this line
        AUTH_USER_MODEL = "main.user"
        ```

- What needs to be *done* after the steps above
    1. *migrations* & *DB tables*

        ```bash
        # ----- Migrations -----

        rm  -fv main/migrations/000*
        rm -rfv main/migrations/__pycache__/


        # ----- PostgreSQL -----
        
        psql

        # Core cmd
            DROP   DATABASE projbooktime;
            CREATE DATABASE projbooktime;

        # Meta cmd
            \l      # check DB list
            \q      # exit cli
        ```

    2. *migrations* 

        ```bash
        ./manage.py makemigrations
        ./manage.py migrate

        ./manage.py createsuperuser     # It'd be 'email' instead of 'username'
        ```

- What now?

    ```bash
    # The default 'username plus password' 
    # now changed to 'email addr plus password' (duh).
    open http://localhost:8000/admin/login/?next=/admin/
    ```


-------------


### Page :: *Registration*
- What needs to be written
    1. *forms*

        ```python
        # We mainly do these two things
        # -- Override  ( general purposes like "name of the model" etc. )
        # -- Override  ( specifically, the "name+pwd  =>  mail+pwd"     )
        
        # Go check the code (detailed comments inside).
        ```

    2. *views*

        ```python
        # Still, the code is quite simple.
        # So I'll just show the structure here :D

        # The Structure (simplified)
        #   1. return to WHERE after you've signed in
        #   2. clean the registration form 
        #   3. authenticate (literally & technically)
        #   4. send email (registration link & success info)
        ```

    3. *templates*

        ```html
        <!-- 
        Ah, quite simple.
            1. Three inputs for {username, password-1, password-2}
            2. One button for "submit"
        -->
        ```

    4. *urls*

        ```python
        path(
            "signup/",
            ..  # view func
            ..  # name used in templates
        )
        ```

- Testing
    - Usage

        ```bash
        # Step 1
        open http://localhost:8000/signup/

        # Step 2
        #   Check terminal messages (should be two, duh).

        # Step 3
        #   Check admin backend
        open http://localhost:8000/admin/main/user/
        ```
    
    - Tests

        ```python    
        # PROJECT/main/tests/test_forms :: TestForm
        # -- test_valid_signup_form_sends_email

        # Expected
        #   There shoudld be a `"Welcome to BookTime"` message
        # How exactly
        #   Send mail with mocked data
        #   Something like `assertEqual(.. "Welcome to BookTime")`
        

        # PROJECT/main/tests/test_views :: TestPage
        # -- test_user_signup_page_loads_correctly
        # -- test_user_signup_page_submission_works

        # WHAT TO TEST
        #   Load page
        #   Post & Authenticate
        ```


### Page :: *Registration*
- A Word
    - The steps are quite *similar* to the steps while creating *registratin page*.
- What needs to be written
    1. *forms*

        ```python
        # We mainly do these things
        # || Two forms added "login page" (email, password)
        # || Override `__init__` => Get the `request` object (sensitive! XD)
        # || Override `clean`    => Auth by provided info (fail-error, termlog-success)
        
        # Go check the code (detailed comments inside).
        ```
    
    2. *settings*

        ```python
        LOGIN_REDIRECT_URL = "/"    # Homepage
        ```

    3. *urls*

        ```python
        from django.contrib.auth import views as auth_views
        from main                import forms

        path(
            "login/",
            auth_views.LoginView.as_view(
                template_name="login.html",
                form_class=forms.AuthenticationForm
            ),
            name="login"
        )
        ```
    
    4. *templates*

        ```html
        <!-- 
        Ah, quite simple.
            1. Two inputs for {username, password}
            2. One button for {submit}
        -->
        ```

- Testing
    - Usage

        ```bash
        # Step 1
        open http://localhost:8000/login/

        # Step 2
        #   IF success  =>  See log msg in terminal
        #   IF failed   =>  Info'll be display above the inputs.
        ```

-----------

### References 
- ```UserAdmin```'s **```add_fieldsets```**
    - [What does UserAdmin's add_fieldsets for? - StackOverflow](https://stackoverflow.com/questions/50436596/django-useradmins-add-fieldsets)
    - [Customizing authentication in Django (Docs|Code)](https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#custom-users-and-django-contrib-admin)
- ```django.contrib.auth.forms.UsernameField```
    - [In Django 1.8, what does "USERNAME_FIELD" mean by auth system? - StackOverflow](https://stackoverflow.com/questions/44028143/in-django-1-8-what-does-username-field-mean-by-authentication-system)