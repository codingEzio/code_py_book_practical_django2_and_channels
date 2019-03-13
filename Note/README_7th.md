
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