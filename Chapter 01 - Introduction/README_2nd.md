
### Customzing *admin* site
- Detailed comments inside the code, go check it out!

### Completing *models* 
- What needs to be fixed
    1. A bit nicer name <small>( instead of ```Product object(N)``` )</small>
    2. **Correctly** serving *user-uploaded* images <small>( return ```404``` for now )</small>
- The code

    ```python
    """ >>> PROJECT/main/models.py <<< """

    class Product(models.Model):
        ...
        def __str__(self):
            return self.name


    """ >>> PROJECT/booktime/urls.py <<< """
    
    from django.conf import settings
    from django.conf.urls.static import static
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```
    
### Management commands
- *Basics*

    ```bash
    # For the sake of simplicity, 
    # some cmds I won't use right now won't be mentioned here.

    ./manage.py             # display all the options you have

    ./manage.py check       # check if everything's fine
    
    ./manage.py shell       # specify by `--interface ipython` (or else)
    ./manage.py dbshell     # open db-related engines (e.g. psql)

    ./manage.py makemessages | compilemessages
    ./manage.py loaddata     | dumpdata
    ```

### Serialization
- Terms
    - *Serialization* : **DB tables** to **File**.
    - *DeSerialization* : **File** to **DB tables**.
- *Dump* & *Load*
    - Issues

        ```bash
        ./manage.py dumpdata --indent 4 main.ProductTag

        # There's an issue here, though,
        # that is some internal IDs lives in the data (e.g. `"products": [4]`)
        ```

    - Inside *Django*

        ```python
        """ >>> PROJECT/main/models.py <<< """

        # Part One
        # -- Place  the `ProductTag` before the `Product` model
        # -- Delete the `.. ManyToManyField(..)` in the `ProductTag`
        # -- Add    the `tags = .. ManyToManyField(ProductTag, ..)` to `Product`

        # Part Two 
        # -- Add two methods to `ProductTag` model

        def __str__(self):
            return self.name 

        def natural_key(self):
            return (self.slug,)
            
        # Part Three
        # -- Add one method to `ProductImage` model
        
        def __str__(self):
            return self.product.name
        ```

    - Outside *Django*
        - WHAT
            - This is the **most** ***goddamn*** import step!!!!
            - Do remember to **make & mig** the DB models after you've made changes to it!
                - Oh, actions like adding a ```__str__()``` does NOT require a *migration* :)
                - It's fine by simply re-running the server.
        - HOW
            
            ```bash
            ./manage.py makemigrations main
            ./manage.py migrate
            ```

    - What now

        ```bash
        # Now you can run it without hidden states
        # and .. well, the changes were ACTUALLY made to databases!
        
        ./manage.py dumpdata \
            --indent 4 main.ProductTag

        ./manage.py dumpdata \
            --indent 4 main.ProductTag \
            --natural-primary \
            > main/fixtures/producttags.json
        ```

- What's more

    ```python
    """ >>> PROJECT/main/admin.py <<< """

    # Since the changes we've made also affected other code
    # we need to modify the 'admin.py' to accommodate it :D

    # ProductTagAdmin :: REMOVE 
    #                 :: autocomplete_fields = ("products",)
    
    # ProductAdmin    :: ADD 
    #                 :: autocomplete_fields = ("tags",)
    ```
    
### *New* management commands
- WHAT
    - ```./manage.py OUR_OWN_COMMAND```
- Getting started
    - Outside of *Django*

        ```bash
        # ---- under 'PROJECT/main/' ---- #

        mkdir management
        touch management/__init__.py 

        mkdir management/commands/
        touch management/commands/__init__.py       
        touch management/commands/import_data.py    # call by `./manage.py import_data`

        # Your structure should like this
        # -- management/
        # -- management/__init__.py
        # -- management/commands/
        # -- management/commands/__init__.py    
        # -- management/commands/import_data.py 
        ```
    
    - "Inside" of *Django*

        ```python

        ```
