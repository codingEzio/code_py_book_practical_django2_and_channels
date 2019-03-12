
### Build tools for *static files*
- More clearly, we'll install these stuff
    1. Bundler
    2. Loader
    3. Framework
- The code 

    ```bash
    npm install -y      # same level as 'manage.py'

    npm install react react-dom         --save
    npm install webpack webpack-cli     --savedev
    npm install webpack-bundle-tracker  --savedev

    pipenv install django-webpack-loader

    
    # Just so you know, after the installation,
    #   there's some modification in the `package.json`.
    ```