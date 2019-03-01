### Tools we'll use 
- **Python** ```3.*```
- **Django** ```2.*```
- *PostgreSQL*
- *pipenv*
    - ```Pipfile``` : All the **direct dependencies** of ur project.
    - ```Pipfile.lock``` : **All** the dependencies with *versions* & *hashes*.

### Getting Started 
- Base
    1. ```mkdir booktime && cd booktime```
    2. ```pipenv --three install Django```
    3. ```pipenv shell```  <small>( activate env )</small>
- Project
    - ```django-admin startproject booktime .``` <small>( under ```booktime``` )</small>
    - ```django-admin startapp main``` 
        - append ```'main.apps.MainConfig'``` to ```INSTALLED_APPS``` <small>( **settings.py** )</small>
- Database
    - *postgreSQL* itself <small>( sort of )</small>
        
        ```bash
        # Get
        brew update && brew install postgresql
        brew services restart       postgresql
        
        # Set
        createuser -dP      projbooktimeuser
        createdb -E utf8 -U projbooktimeuser projbooktime
        
        # Driver
        pipenv install psycopg2-binary  # http://initd.org/psycopg/docs/index.html
        
        # GUI
        # I myself was using Navicat (for postgreSQL).
        ```
        
    - *postgreSQL* Django's side

        ```python
        DATABASES = {
            'default': {
                'ENGINE'  : 'django.db.backends.postgresql',
                'NAME'    : 'projbooktime',
                'USER'    : 'projbooktimeuser',
                'PASSWORD': 'whatever',
                'HOST'    : '127.0.0.1',
                'PORT'    : '5432',                           # default
            }
        }
        ```

----------

### Get our first page *running*
- **Setup** outside *Django*

    ```bash
    # ---- ALL UNDER 'PROJECT/app-main' ----
    
    # [Templates]
    
    mkdir templates && cd templates 
    touch home.html
    
    # [Static files]
    
    mkdir -p static/js 

    curl -o jquery.min.js     https://code.jquery.com/jquery-3.2.1.slim.min.js 
    curl -o popper.min.js     https://unpkg.com/popper.js@1.12.9/dist/umd/popper.min.js
    curl -o bootstrap.min.js  https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js
    
    mkdir -p static/css
    
    curl -o bootstrap.min.css https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css
    ```

- **Setup** inside *Django*

    ```python
    """ PROJECT/booktime/urls.py """
    
    from django.views.generic import TemplateView
    
    urlpatterns = [
        path( .. ),
        path('', TemplateView.as_view(template_name="home.html"))
]

    """ PROJECT/main/templates/home.html (examples) """
    
    {% load static %}
    
    # CSS
    #   old:  <link .. href="CDN_CSS_LINK">
    #   new:  <link .. href="{% static 'css/bootstrap.min.css' %}">
    
    # JS
    #   old:  <script .. src="CDN_JS_LINK"> ..
    #   new:  <script .. src="{% static 'js/bootstrap.min.js' %}"> ..
    ```

- Issues 
    1. It might return a ```404 Not Found``` <small>( inside **DevTools** )</small> for those *static* files 
        - Delete strings like ```/*# sourceMappingURL .. */``` either in *JS* or *CSS* files.
        - **Un-check** one of the settings in *DevTools* which is called **Enable JavaScript source maps**.


### Get our first test *passed*
- Inside *Django*

    ```python
    """ PROJECT/main/tests.py """
    
    class TestPage(TestCase):
        def test_home_page_works(self):
            response = self.client.get("/")
    
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "home.html")
            self.assertContains(response, "BookTime")
            

    """ PROJECT/main/templates/home.html """
    
    # A little modification for getting the test passed
    #   old:  <title> Hello, Django! </title>
    #   new:  <title> BookTime       </title>
    ```

- Outside *Django*

    ```console
    foo@bar:~$ ./manage.py test
    ...
    ```

### Those do not worth taking notes
1. A **base templates** for all the other pages.
2. A bit of *style* for our page <small>( **Bootstrap** for now, you're free to use the others )</small>
3. Seperated ```urlpatterns``` <small>( project | apps )</small>
4. Decoupling the *request URLs* while doing testing <small>( ```urlpattern``` > ```name``` < ```reverse``` )</small>

### Restructing the *tests*
- Like this 
    
    ```bash
    # old:
    #     PROJECT/app-main/tests.py
    
    # new:
    #     PROJECT/app-main/tests/ 
    #     -- __init__.py
    #     -- test_views.py      # the original 'tests.py'
    #     -- test_forms.py      # new test file our forms (HTML widgets)
    ```

- Controlling **verbosity** while testing
    
    ```bash
    ./manage.py test -v 0    # minimal 
    ./manage.py test -v 3    # very verbose
    ```
    
- Controlling **how many tests** to run <small>( *scope* might be more appropriate )</small>

    ```bash
    # All | App | App-feature
    
    ./manage.py test
    
    ./manage.py test main
    ./manage.py test main.tests
    
    ./manage.py test main.tests.test_views
    ./manage.py test main.tests.test_views.TestPage
    ./manage.py test main.tests.test_views.TestPage.test_about_page_works
    ```

- Additional arguments for us to use
    - ```--failfast```
    - ```--keepdb```
    - For more to check official doc: [writing and running tests](https://docs.djangoproject.com/en/2.1/topics/testing/overview/)

### The *Contact Us* page
- Five aspects
    1. *views*, *forms*, *templates*
    2. *urls*, *tests*
- So..
    - Since the code|structure is **quite easy to understand**,
    - I'll just omit the explanation for now <small>( I **might** add it in the future )</small>.

----------

### Get our first <small>( 3 )</small> *models* migrated
- **Setup** inside *Django*

    ```python
    """ PROJECT/main/models.py """
    
    # Base | BaseAttr | BaseAdvanced
    
    class Product(models.Model):
        pass
    
    class ProductImage(models.Model):
        pass
        
    class ProductTag(models.Model):
        pass
    ```

- **Setup** outside *Django*
    
    ```bash
    # Do make migrations for each model.
    # e.g.
    #   1.1 write 'Product' 
    #   1.2 make migrations
    #   2.1 write 'ProductImage'    # Run `pipenv install Pillow`
    #   2.2 make migrations         # before you're migrating the fields!
    #   3.1 ...
    
    # Migrate
    ./manage.py makemigrations      # You'll run it 3 times in total 
    
    # Migrate, for real
    ./manage.py migrate             # Run this after you've written & makemig (3 times)
    ```  
 
### Making *thumbnails*
- **Setup** inside *Django*

    ```python
    """ PROJECT/main/models.py :: `ProductImage` """
    
    thumbnail = models.ImageField(
        upload_to="product-thumbnails", null=True
    )
    
    
    """ PROJECT/main/signals.py """
    
    # 1. get product instance
    # 2. using 'PIL' to manipulate the images
    # 3. xx.save()
    
    
    """ PROJECT/main/apps.py :: `MainConfig` """
    
    class MainConfig(AppConfig):
        name = "main"
    
        # This method make sure the `signals.py` 
        # is initialized when the Django app is launched
    
        def ready(self):
            from . import signals


    """ PROJECT/booktime/settings.py """
    
    # Do make sure you've got these 2 lines
    
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    ```

- **Setup** outside *Django*
    
- Tests for ```signals.py``` <small>( whether the *conv-thumbnail* works or not )</small>

    ```python
    # Preparation
    #   1. Make sure you've got the sample pics  ( ../Apress/practical-django2-and-channels2 )
    #   2. Copy the pics to the right place      ( under '../main/fixtures' )
    
    # Writing tests
    # -- WHERE  PROJECT/main/tests/test_signals.py
    # -- WHAT   I omitted the code since it's not that complicated.
    ```
    
### *QuerySets* & *Manager*
- I'll complete the former one later on :D
- Adding *Manager* to our model
    
    ```python
    class ActiveManager(models.Manager):
        def active(self):
            return self.filter(active=True)

    class Product(models.Model):
        # ...
        objects = ActiveManager()
    ```

- Adding *Manager* tests 

    ```python
    """ PROJECT/main/tests/test_models.py """

    from .. import ..
    from .. import ..

    class TestModel(TestCase):
        def test_active_manager_works(self):
            """ It's quite simply I'd say ..
            """
            
            models.Product.objects.create(.. , )
            models.Product.objects.create(.. , )
            models.Product.objects.create(.. , active=False)
            
            self.assertEqual(len(models.Product.objects.active()), 2)
    ```



----------

### Practices <small>( order by *TIME* )</small>
1. **Re-deployed** ur project if you've made changes to ```settings.py```
2. By using ```context_processors```, you would reduce lots of work to require vars in every view.
3. Do keep the ```SECRET_KEY``` in a goddamn-safe place while go production mode!!!
4. About *Function-* and *Class-Based* views
    - Features
        - One for *no hidden behavior*, *quite easy-to-understand*
        - One for *add code to change default*, *don't have to re-impl everything*.
    - So WHAT
        - Both have their own merits. No clear winners apparently :)
        - It'll be whole a lot easier **if you've writing** *automated* | *unit* **tests all the time**.
5. Recommended activity loop: 
    - writing **code** 
    - writing **tests** && running **tests**
        - *good-to-go* -> **coding**
        - *failure* -> **fixing**
            - running **tests**
                - *good-to-go* -> **coding**
                - *failure* -> **fixing**

### *Just So You Know*
- *Regex* ```urlpatterns``` is still being supported
    
    ```python
    re_path(r"^product/(?P<id>[^/]+)/$",
            TemplateView.as_view(template_name="home.html")),
    ```

- 

----------

### References
- [stackoverflow :: Offiline static files :: Use 'min.X' not 'map.X'](https://stackoverflow.com/questions/21773376/bootstrap-trying-to-load-map-file-how-to-disable-it-do-i-need-to-do-it)
- [Django Signals - an Extremely Simplified Explanation for Beginners](https://coderwall.com/p/ktdb3g/django-signals-an-extremely-simplified-explanation-for-beginners)