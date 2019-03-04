
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

    ./manage.py flush       # Ah! This one is my FAVORIATE
                            # It simply reverts the whole DB to its original state
                            # That means you don't need to "del-and-create" manaualy!
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
    - ```./manage.py OUR_OWN_COMMAND PARAM_1 PARAM_2```
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
        # ---- under 'PROJECT/main/management/commands/import_data.py' ---- #
        
        # I'll just put the structures here,
        # since the full implementation is quite long :P

        """ 
        Okay, how?
            1. Import the packages we need
            2. Add command-line arguments  
            3. Load data from CSV|Image files
            4. Create objects by the loaded data
            5. Display some progres info (`stdout.write`)
        """
        ```

- Let's *test* it
    - Preparation
        - Make sure you've downloaded the samples <small>( [Official Repo](https://github.com/Apress/practical-django2-and-channels2) )</small>.
        - Then copy the files needed to ```PROJECT/main/fixtures/```
            1. ```product-sample.csv```
            2. ```product-sampleimages/``` <small>( three pics inside )</small>
    - Usage
        
        ```bash
        ./manage.py import_data YOUR_CSV_FILE_PATH YOUR_IMAGES_FILE_PATH
        ```

    - The tests

        ```python
        """ >>> PROJECT/main/tests/test_import.py <<< """

        # Nothing fancy.
        
        # Just so you know, I commented a few lines 
        # to get the tests passed (i.e. the "tag" part).

        # What changes I made, EXACTLY?
        # -- the COMMAND 
        # -- the test file 

        # I don't really changed the functionality
        # I just commended lines like 'stdout.write'.
        ```
        
### 