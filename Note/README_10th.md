### Printing Order *invoices*
- Basics

    ```bash
    # You might need to install sth else depending on ur system.
    pipenv install WeasyPrint
    ```

- *admins*

    ```python
    # Docoupling this feature as ONE mixin for other classes to use.
    #   which is, the `class InvoiceMixin` (without any superclass, btw).
    
    class InvoiceMixin:

        def ..(..):

            ..
            .. "invoice/<int:order_id>/"
            .. self.admin_view(self.invoice_for_order)
            ..


        def invoice_for_order(..):

            # 1. Get THE order
            # 2. To know whether the user wants PDF (or simply HTML)
            # 3. RETURN { PDF -> return response, HTML -> render Invoice.html }
            # 4. Configure 'WeasyPrint' (URI, Header)
            # 5. Writing the PDF as a temporary file (using stdlib)


    class OwnersAdminSite           ( InvoiceMixin , .. ):
        ..
        ..

    class CentralOfficesAdminSite   ( InvoiceMixin , .. ):
        ..
        ..

    ```

- *templates* :: **Content** page

    ```html
    <!-- PROJECT/main/templates/ :: invoice.html -->

    <!-- 

        Pretty easy though,
        1. Importing CSS
        2. Add header
        3. Add data (using 'table' layout)
        4. Add footer
    -->
    ```

- *templates* :: **Invoice** interface at *admin site*

    ```html
    <!-- PROJECT/templates/admin/ :: main/order/ :: invoice.html -->

    <!--
        Since we're <overriding> the templates (for admin site)
        we don't have to write too much code actually :D

        Here you are:
		..  <a href="{{ invoice_url }}"              >   ..
		..  <a href="{{ invoice_url }}?format=pdf"   >   ..
    -->
    ```