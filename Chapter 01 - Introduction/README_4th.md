
### *Addresses*
- We will need **users' addresses** since the *checkout* feature still accounts for that.
- Here's how we do
    1. *models*

        ```python
        class Address(models.Model):
            user     = ..
            name     = ..
            address1 = ..
            address1 = ..
            zip_code = ..
            city     = ..
            country  = ..

            def __str__(self):
                return ", ".join([
                    .. , .. , .. ,
                    .. , .. , .. ,
                ])
        ```

    2. *migrations*

        ```bash
        ./manage.py makemigrations
        ./manage.py migrate
        ```

    3. *views*

        ```python
        # Letting user to {ADD, REMOVE, CHANGE} their addrs.

        from django.urls import reverse_lazy
        from django.contrib.auth.mixins import LoginRequiredMixin
        from django.views.generic.edit import ( FormView   ,
                                                CreateView ,
                                                UpdateView ,
                                                DeleteView , )


        class AddressListView  ( MIXIN {LOGIN, related}):
            ..

            .. objects.filter .. request.user

        class AddressCreateView( MIXIN {LOGIN, related}):
            ..

            fields      = ...
            success_url = ...

            def form_valid( .. ):
                ..
                ..   # save

        class AddressUpdateView( MIXIN {LOGIN, related}):
            ..

            fields      = ...
            success_url = ...

            def ..
                return .. objects.filter .. request.user


        class AddressDeleteView( MIXIN {LOGIN, related}):
            ..

            success_url = ...

            def ..
                return .. objects.filter .. request.user
        ```

    4. *urls*

        ```python
        path("address/",
             views.AddressListView.as_view()   , name="address_list"   ) ,

        path("address/create/",
             views.AddressCreateView.as_view() , name="address_create" ) ,

        path("address/<int:pk>/",
             views.AddressUpdateView.as_view() , name="address_update" ) ,

        path("address/<int:pk>/delete/",
             views.AddressDeleteView.as_view() , name="address_delete" ) ,
        ```

    5. *templates*

        ```html
        <!-- 
            All the related files are under < PROJECT/main/templates/main/ >
            -- address_list.html
            -- address_form.html
            -- address_update.html
            -- address_confirm_delete.html
        -->

        <!-- 
            address_list.html 
        
            1. Loop the addresses
            2. Links for 'Update address', 'Delete address'
            3. Link  for 'Add new address' (outside of above)


            address_form.html 
        
            1. The fields were come from 'views' (it controls what to display)
            2. And the functionalities was mostly done by {ourOverrides, Mixins}.


            address_update.html 
        
            1. The fields were come from 'views' (it controls what to display)
            2. And the functionalities was mostly done by {ourOverrides, Mixins}
            3. The templates for {form, update} is the same.
               Yet, the "mechanics" was done by Mixins (CreateView, UpdateView).
        

            address_delete.html

            1. It contains <AreYouSureToDelete, submitToDelete> (summary).
        -->
        ```

- And the *tests*, of course.

    ```python
    """ Location :: main/tests/test_views.py :: TestPage """

    def test_address_list_page_returns_only_owned():
        # 1. Create user
        # 2. Assign 'addresses' stuff to the user
        # 3. Login with one of them & test if the "filter" works

    def test_address_create_stores_user():
        # 1. Create user
        # 2. Login
        # 3. Post date & test if it's there

    ```