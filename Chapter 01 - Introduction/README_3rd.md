
### Page :: *Product List*
- What needs to be written
    1. *views*

        ```python
        # For the sake of simplicity, I won't show all the code here.

        # Specify
        # -- templates location
        # -- paging num by your need 

        # Also, you could specific tags, or not.
        # the params was given while you're accessing the URL.
        if self.tag:
            .. filter(tags=self.tag)
        else:
            .. 
        ```

    2. *urls*

        ```python
        # Just to make sure the routes will work
        app_name = "main"

        path(
            "products/<slug:tag>/",
            ..  # view func
            ..  # name used in templates
        )
        ```

    3. *templates*

        ```html
        <!-- 
        Still, for the sake of brevity, I'll only show a little bit of it.

        The code down below is kinda hard-to-understand (for me)
        
            `page_obj`          related to `paginate_by` in our view
            `main:products`     APP_NAME:URLPATTERN_NAME (err in book)
        -->

        {% for product in page_obj %}
            ...

            {{ product.name }}

            {% url 'main:product' product.slug %}

            ...
        {% endfor %}
        ```

- Testing
    - Usage

        ```bash
        # Preq
        # 1. The 'slug' cannot be null for the related tag.
        # 2. What you've passed is "the slug" (slugified tag).

        open http://localhost:8000/products/all/
        open http://localhost:8000/products/open-source/
        ```
    
    - Tests

        ```python    
        # PROJECT/main/tests :: TestPage
        # -- test_products_page_returns_active
        # -- test_products_page_filters_by_tags_and_active

        # Nothing fancy, just these steps:
        # 1. create objects
        # 2. `client.get` the page (like a real user)
        # 3. do asserting (e.g. `assertEqual`, `assertContains`)
        ```
    
- Oh, one more thing!
    - Since I've added the ```app_name = 'main'``` to ```urls.py```
    - There's some changes you need to made (in tests)

        ```python
        self.client.get(reverse(     "contact_us"))    # OLD
        self.client.get(reverse("main:contact_us"))    # NEW
        ```


### Page :: *Single Product*
- What needs to be written
    1. *templates*

        ```html
        <!-- 
        Ah, the template itself is quite simple.
        Just with more "template filters" this time.

        Something like this
            object.description|linebreaks
            object.in_stock|yesno|capfirst
            object.date_updated|date:"F Y"
            object.tags.all|join:","|default:"No tags availabel :("
        -->

        <!-- 
        Oh, also the book got some errors (or not)
            {% url 'add_to_basket' %}?product_id={{ object.id }}
        
        Since we (and the book) havn't impl it yet,
        you need to change the value of `href` to "#" (at least temporarily).
        -->
        <a href="#">
		    Add to basket
	    </a>
        ```
    
    2. *urls*

        ```python
        from django.views.generic.detail import DetailView
        from main import models

        path(
            "product/<slug:slug>/", 
            DetailView.as_view(model=models.Product),   # How convinient!
            name="product"                              # used in templates
        )
        ```

- Testing <small>( *usage* as well )</small>
    
    ```bash
    # Ah, the name could be different from yours, though.
    
    open http://localhost:8000/product/siddhartha/
    open http://localhost:8000/product/backgammon-for-dummies/
    open http://localhost:8000/product/the-cathedral-and-the-bazaar/
    ```
