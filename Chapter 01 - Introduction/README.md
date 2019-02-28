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
        pipenv install psycopg2  # http://initd.org/psycopg/docs/index.html
        
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
    """ PROJ/booktime/urls.py """
    
    from django.views.generic import TemplateView
    
    urlpatterns = [
        path( .. ),
        path('', TemplateView.as_view(template_name="home.html"))
]

    """ PROJ/main/templates/home.html (examples) """
    
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

### Practices
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

### References
- [stackoverflow :: Offiline static files :: Use 'min.X' not 'map.X'](https://stackoverflow.com/questions/21773376/bootstrap-trying-to-load-map-file-how-to-disable-it-do-i-need-to-do-it)