
### External libraries
- Let's try the **```django-extensions```**

    ```bash
    # ----- Terminal -----

    pipenv install django-extensions
    
    pipenv install pydotplus    # for 'graph_model'     
    pipenv install ipython      # for 'shell_plus' 
    pipenv install werkzeug     # for 'runserverplus' 


    # ----- settings.py -----

    INSTALLED_APPS = [
        .. ,
        .. ,
        "django_extensions",
    ]

    
    # ----- Terminal -----

    # They were integrated into the `./manage.py` command
    # e.g.
    #       ./manage.py shell_plus
    #       ./manage.py runserver_plus
    #       ./manage.py graph_models -a -o OUTPUT_PICTURE.png
    ```

- Generating *fake* data for tests

    ```python
    # ----- Terminal -----
    
    pipenv install factory_boy


    # ----- PROJECT/main/       :: factories.py -----
    
    class ProductFactory(factory.django.DjangoModelFactory):
        """ There're also other examples, here's just a glimpse.
        """

        price = factory.fuzzy.FuzzyDecimal(1.0, 1000.0, 2)

        class Meta:
            model = models.Product


    # ----- PROJECT/main/tests  :: test_models.py -----

    # 1. Import the 'factories.py'
    # 2. Replace the hard-coded data with sth like `factories.xxFactory(PARAM)`
    ```

- *Django Debug Toolbar*

    ```python
    # It's a lib that display useful info about the loaded web page,
    # such as
    # || HTTP request/response
    # || Django internal settings
    # || SQL queries triggered
    # || Templates used
    # || Cache calls etc.

    # ----- Install & Config (settings.py) -----

    # 1. pipenv install django-debug-toolbar

    # 2. INSTALLED_APPS
    INSTALLED_APPS = [
        .. ,
        .. ,
        "debug_toolbar",
    ]

    # 3. MIDDLEWARE
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        .. ,
        .. ,
    ]

    # 4. INTERNAL_IPS
    INTERNAL_IPS = ["127.0.0.1"]

    
    # ----- One more config in 'PROJECT/booktime/urls.py' -----

    if settings.DEBUG:
        import debug_toolbar

        urlpatterns = [
                          path("__debug__/", include(debug_toolbar.urls))
                      ] + urlpatterns


    # ----- What does it look like -----

    # It'll be displayed in EVERY page, aha!
    ```


### Visualizing *Orders*
- Preparation

    ```python
    # ----- Terminal -----

    pipenv install django-tables2
    pipenv install django-filter
    

    # ----- Register & Config -----

    INSTALLED_APPS = [
        .. ,
        .. ,
        "django_tables2",
        "django_filters",
    ]

    DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap.html"
    ```


- Writing *views*

    ```python
    from django import forms as django_forms
    from django.db import models as django_models
    from django.contrib.auth.mixins import UserPassesTestMixin
    
    import django_filters
    from django_filters.views import FilterView


    class DateInput     (..):
        """ Selecting 'date'
        """

        ..

    
    class OrderFilter   (..):
        """ What to filter, what condition to filter with etc.
        """
        
        ..

    
    class OrderView     (..):
        """ Using the filters above & restricting access (admin staff only)
        """

        ..
    ```

- Writing *templates*

    ```html
    {% extends "base.html" %}
    {% load render_table from django_tables2 %}

    {% block content %}
	    <h2>Order dashboard</h2>

    	<form method="GET">
    		{{ filter.form.as_p }}    <!-- Most work were done by 'views.py' -->
    		<input type="submit" />
    	</form>

    	.. {% render_table filter.qs %} ..
    {% endblock content %}
    ```

- Writing *urls*

    ```python
    path(
        "order-dashboard/",
        views.OrderView.as_view(), 
        name="order_dashboard")
    )
    ```

- Testing
    
    ```bash
    # 1. Make sure you've added some addresses 
    # 2. Do some purchases (checkout)
    # 3. Go 'http://localhost:/8000/order-dashboard' 
    ```


-----------


### Tweaking *widgets*
- Preparation

    ```python
    # 0. What does it do?
    # --- Modify the CSS/HTML stuff without touching code (forms.py).
    # --- We'll modify the templates using the "tags" provided by it.


    # 1. Install
    pipenv install django-widget-tweaks

    # 2. Config
    INSTALLED_APPS = [
        .. ,
        .. ,
        "widget_tweaks",
    ]
    ```

- Modifying the *templates*

    ```html
    <!-- 
        main/templates/ :: include/forms.html

        main/templates/
        || login.html
        || signup.html
        || contact_form.html

        Go check the code for more details.
    -->
    ```
