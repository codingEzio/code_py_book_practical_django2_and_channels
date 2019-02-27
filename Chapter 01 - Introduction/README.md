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


### Practices
1. **Re-deployed** ur project if you've made changes to ```settings.py```
2. By using ```context_processors```, you would reduce lots of work to require vars in every view.