### Foreword
- In short, we're gonna **customizing** ***admin*** **site** in this chapter.
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