### A better *widget* 
- which is used for changing **quantity** of products in the basket.
- Here's how we do it
    
    1. *widgets*

        ```python
        # There're related FOUR files
        # || widgets.py              # Specify the modified template ( CSS, JS included )
        # || plusminusnumber.html    # Basic 'one-input & two-btns'  ( behavior changes, though )
        # || plusminusnumber.css     # Replace the default with our own buttons
        # || plusminusnumber.js      # Functionalities for buttons (plus|minus) ( & related input )
        
        # Go check the code, XD!
        # The 'widgets.py' is just like a "form", but smaller, abstractly.
        ```
       
    2. *forms*

        ```python
        BasketLineFormSet = inlineformset_factory(
            .. ,
            .. ,
            .. ,
            .. ,
            widgets={ "quantity" : widgets.PlusMinusNumberInput() }    # our customized 'input'
    )
        ```
        
    3. *templates*

        ```html
        <!-- 
            PROJECT/main/templates :: base.html
        -->
        
        {% block js %}
        {% endblock js %}
        
        
        <!-- 
            PROJECT/main/templates :: wigets/plusminusnumber.html
        -->
        
        {% block js %}
    	      {% if formset %}
    		        {{ formset.media }}
	          {% endif %}
        {% endblock js %}
        ```