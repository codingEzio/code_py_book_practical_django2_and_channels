
### Build tools for *static files*
- More clearly, we'll install these stuff
    1. Bundler
    2. Loader
    3. Framework
- Base

    ```bash
    npm install -y      # same level as 'manage.py'

    npm install react react-dom         --save
    npm install webpack webpack-cli     --savedev
    npm install webpack-bundle-tracker  --savedev

    pipenv install django-webpack-loader

    
    # Just so you know, after the installation,
    #   there's some modification in the `package.json`.
    ```

- Config

    1. *Webpack* config

        ```bash
        # WHERE     same level as 'manage.py'
        # NAME      'webpack.config.js'
        ```

    2. *Webpack* config :: **Django**

        ```python
        # PROJECT/booktime/settings.py 

        # 1. INSTALLED_APPS     ..
        # 2. WEBPACK_LOADER     ..
        ```

    3. Decouple the *CSS* & *JS* from the templates

        ```javascript
        /*
        ORIGINAL        PROJECT/main/templates/main/product_detail.html
        DESTINATION     PROJECT/frontend/imageswitcher.js

        Note
            Just go check the code. Too damn hard to make it work :P
            
            After you've done that, 
            run `npm run build` at PROJECT level.
        */ 
        ```

- Issues
    1. Bunch of errors out there, ah..
    2. IT JUST DOESN'T WORK <small>( switch-image )</small>
    3. This part is such a mess that I'll just *skip* this part without too much details :(