### Review
- Okay, okay.. Now we've solved some *nasty* bugs.
- There's still one <small>( & **only one** )</small> is yet to be solved, which is
    - The *image switching* feature, yep, it has no effect if u clicked on them
    - Ah, the most weird one is that **the tests passed** <small>( with some *path* issues, though )</small>
- So?
    - I'll skip that for now <small>( since the *py* | *js* tests could pass :P )</small>
    - And it's really not a big deal since it doesn't affect the **core features**.

--------

### Building *API*s using **Django REST Framework**
- Here's how we *gonna* use it <small>( though we havn't impl it.. )</small>

    ```bash
    # Orders :: ready to be shipped

    curl -H 'Accept: application/json; indent=4' \
         -u EMAIL_ADDR:EMAIL_PASSWD   \
         http://localhost:8000/api/orderlines


    # Orders :: shipping address of the specific order

    curl -H 'Accept: application/json; indent=4' \
         -u EMAIL_ADDR:EMAIL_PASSWD   \
         http://localhost:8000/api/orders/2   


    # Orders :: update the status of the order lines 

    curl -H 'Accept: application/json; indent=4' \
         -u EMAIL_ADDR:EMAIL_PASSWD   \
         -XPUT                                   \
         -H 'Content-Type: application/json'     \
         -d '{"status": 20}'                     \
         http://localhost:8000/api/orderlines/2

    
    # Orders :: check 'orders' after making changes to the status

    curl -H 'Accept: application/json; indent=4' \
         -u EMAIL_ADDR:EMAIL_PASSWD   \
         http://localhost:8000/api/orderlines       # same as the 1st one!
    ```

- Okay, let's build it!  <small>( *foundation* )</small>
    
    - Base

        ```python
        # Here's the steps
        #   0. pip                          pipenv install djangorestframework
        #   1. settings.py                  INSTALLED_APPS :: "rest_framework"
        #   2. settings.py                  ↓ down below ↓
        #   3. proj/booktime/urls.py        path("api-auth/", include("rest_framework.urls"))
        
        REST_FRAMEWORK = {
            "DEFAULT_AUTHENTICATION_CLASSES": ( .. , .. ),    # REST
            "DEFAULT_PERMISSION_CLASSES"    : ( .. ,    ),    # REST
            "DEFAULT_FILTER_CLASSES"        : ( .. ,    ),    # 3rd-party
            "DEFAULT_PAGINATION_CLASSES"    : ( .. ,    ),    # REST
            "PAGE_SIZE"                     : 100,
        }
        ```

    - Writing *endpoints*

        ```python
        # It lives at the same place as 'views.py'.

        # Both're API-related:
        # || Serializer     Order, OrderLine
        # || ViewSet        Order, OrderLine
        ```

    - Writing *urls*

        ```python
        from django.urls    import include
        from rest_framework import routers
        from main           import endpoints

        outer = routers.DefaultRouter()

        router.register(r"orderlines" , endpoints.PaidOrderLineViewSet)
        router.register(r"orders"     , endpoints.PaidOrderViewSet    )


        urlpatterns = [
            .. ,
            .. ,
            path("api/", include(router.urls))
        ]
        ```

    - Writing *signals*

        ```python
        # What we wanna do is that
        # <Mark> the order as 'DONE' if all the "orderline items" were "SENT".

        @receiver(post_save, sender=OrderLine)
        def orderline_to_order_status( .. , .. , .. ):
            
            if ( .. )
                logger.info( .. )

                instance.order.status = Order.DONE
                instance.order.save()
        ```

- Testing

    ```bash
    # Well, you got two ways to test 
    #   Either from 'http://localhost:8000/api/'
    #   Or          using the `curl` commands above (which is recommended)

    # Right now, it seems that it doesn't work correctly
    # [ ] Might be *in-adequate* sample data    ***
    # [ ] Might be *anything-else*              **
    # [ ] Might be *proxy* issues (socks-5)     *
    
    # Still, I'll leave this here right now
    #   I'll try solve this issue
    #   if it's used by the following content.
    ```