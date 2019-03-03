
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