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
