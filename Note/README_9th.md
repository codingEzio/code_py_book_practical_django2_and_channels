### Customizing different *admin-site* for different roles
- About *admin backend*

    ```bash
    # Check all the available routes (using 'django_extensions')
    ./manage.py show_urls 
    ./manage.py show_urls | grep "admin/"
    ./manage.py show_urls | grep "admin/" | grep -v "main"

    # Some of them which we've seen the most 
    #   -- Index view         Models all
    #   -- App list view      Models that belongs to specific app
    #   -- Add view           Directly add  specific model (ah)
    #   -- Change view        Directly edit specific model (ah)
    #   -- Change list view   Directly edit specific model's instance
    #   -- Delete view        Warning msg|prompt when you're deteling the records
    #   -- History view       History for each of the models' instance
    #   -- Support view       Home-page | Log-in | Log-out etc.

    # Just so you know :)
    # [1] Those "views" lived under '../site-packages/django/contrib/admin/templates/'
    # [2] We CAN have multiple admin interfaces (which is `django.contrib.admin.site`)
    ```

- Next, we'll do some preparations for the *multiple admin sites*

    ```python
    # What we're gonna do   =>  Different backends for different types of roles
    
    # What roles do we need   
    #   || Owners           =>  See|Operate-all-models
    #   || Central office   =>  Flag-order-as-PAID, Order-data, Site-perfm, Prod-related-info
    #   || Dispatch office  =>  Flag-orderline-as-SHIPPED|CANCELED, Flag-prod-as-OUT-OF-STOCK
    
    # What roles do we need, pragmatically
    #   || Owners           =>  Owners          (group)
    #   || Central office   =>  Employees       (group)
    #   || Dispatch office  =>  Dispatchers     (group)

    # How to CREATE them
    #   0. No need to do this manually
    #   1. Clone the offical repo, copy the 'app-main/data/' to your 'app-main/'
    #   2. The filename is 'user_group.json', just so you know.
    #   3. Import the data by `./manage.py loaddata main/data/user_groups.json`
    ```

- And add two more methods for **identifying what type of users is**

    ```python
    # PROJECT/main/models.py :: User (put the code at the bottom)
    
    class User(AbstractUser):
        ..
        ..

        @property
        def is_employee(self):
            """
            Requirements
            1. ACTIVE and CAN_ACCESS_ADMIN
            2. One of the three types of user ( .. | Employees | Dispatchers )
            """

            return self.is_active and (
                self.is_superuser or self.is_staff
                and self.groups.filter(name="Employees").exists()   # same syntax for 'Dispatchers'
            )
    ```

- Implementing the core stuff <small>( **```admin.py```** )</small>

    ```python
    # Part X
    #   1. Import modules
    #   2. Code clean-up

    # Part One
    #   1. ProductAdmin       :: MOD-NEW-two    => Limit [the-ability-to-change-slug]
    #   2. DispatchersProductAdmin :: ADD-one   => ?
    #   3. ProductTagAdmin    :: MOD-NEW-two    => Limit [the-ability-to-change-slug]
    #   4. AddressAdmin       :: NEW-NEW-two    => { list_display, readonly_fields }
    #   5. UserAdmin          :: MOD-DEL-one    => { @admin.register(models.User) }
    #   6. OrderAdmin         :: MOD-DEL-one    => { @admin.register(models.Order) }
    #   7. BasketAdmin        :: MOD-DEL-one    => { @admin.register(models.Basket) }
    #   8. ..register(..)     :: MOD-DEL-three  => cuz overlapping funcs (role `Owners`)

    # Part Two
    #   1. Admin :: { CentralOfficeOrderLineInline, CentralOfficeOrderAdmin } (duh)
    #   2. Admin :: { DispatchersOrderAdmin } (less fields available cuz its perm)
    #   3. Helper|Extra :: { ColoredAdminSite, ReportingColoredAdminSite }
    
    # Part Three
    #   1. OwnersAdminSite              # Same format with different params 
    #   2. CentralOfficesAdminSite      # CUSTOMIZATION: [style, is_WHAT_ROLE]
    #   3. DispatchersAdminSite         # < is_WHAT_ROLE ~ what_perm_does_it_have >

    # Part Four
    #   1. Initilize with the helpers above (for `register`)
    #   2. Three types in total
    #       -- main_admin               (overlaps with former `admin.site.register`)
    #       -- central_office_admin
    #       -- dispatchers_admin
    ```

- Override the *templates* <small>( *admin* )</small>

    ```python
    # booktime/settings.py :: TEMPLATES :: 'DIRS' :: MODIFY

    TEMPLATEs = [
        .. : .. 
        .. : .. 

        'DIRS': [ os.path.join(BASE_DIR, "templates") ]
    ]


    # booktime/templates/ (proj level apparently)
    # || ../admin/base_site.html    duh~
    # || ../admin/index.html        I directly copied it from the offical repo, XD

    # The 1st : it's kinda an admin-style `base.html`
    # The 2nd : $VIRTUAL_ENV/lib/py*3.?/site*/dj*/cont*/admin/templates/admin/index*

    # What does these two do, exactly?
    # || Home page for ADMIN
    # || Base tmpl for ADMIN
    ```

- Routes for different admin sites <small>( **```urls.py```** )</small>

    ```python
    # booktime/urls.py :: MODIFY

    """
    OLD     path("admin/", admin.site.urls)

    NEW     from main import admin

            path("admin/", admin.main_admin.urls),
            path("office-admin/", admin.central_office_admin.urls),
            path("dispatch-admin/", admin.dispatchers_admin.urls),
    """
    ```

### Additional features for *admin* sites
- *Reports* for all

    ```python
    # Part of the job was done by 'admin.py' (ReportingColoredAdminSite)
    # 1. URL routes             `get_urls`   
    # 2. Data for plotting      `orders_per_day`

    """ PROJECT/main/templates/ :: orders_per_day.html """
    # 1. Using the base templates of 'admin site' (under 'proj/templates/admin/')
    # 2. Importing JavaScript library (Chart.js)
    # 3. Init a canvas board & ready to draw
    # 4. Load data & do some configuration
    # 5. DONE!
    ```

- 