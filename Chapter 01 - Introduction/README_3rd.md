
### Display the *product list*
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
