### Foreword
- Starting from this chapter, we'll build something more *complicated*.
    - Such as these topics
        - Redis
        - WebSocket
        - Django *Channels*
- Some basics
    1. About *Django Channels*
        
        > *Channels* allows us to write **asynchronous** code to deal with  incoming requests,<br>
        > &nbsp;&nbsp;which is helpful is case we have a naturall async     interaction between C|S, e.g. A *chat session*

    2. About *Redis*
        - It would be mainly used by *Django Channels*, including these uses
            - **Pass messages** between different *instances* of the running Django app
            - Do **message passing** between inst running on *different machines* OR a *single server*
            - Do **communication between processes**
    
    3. About *Consumers* <small>( Term in *Channels* )</small>

        - It's like *class-based views*,
            - from my perspective, it is <u>*core stuff have been implemented*</u> & <u>*customizing through override*</u>.
            - Two base *consumer* classes, ```SyncConsumer``` and ```AsyncConsumer```. 
            - Other deriatives
                - ```WebsocketConsumer``` and ```AsyncWebsocketConsumer```
                - ```JsonWebsocketConsumer``` and ```AsyncJsonWebsocketConsumer```
                - ```AsyncHttpConsumer```
        - The structure of consumers is based on 
            1. a comb of msg handlers <small>( class methods )</small> AND the ```send()``` built-in method. 
        - Consumers can have multiple message handlers
        - The routing of messages is based on the type value of the message.

    
- Pre-read
    1. [RTD :: Asyncio](https://asyncio.readthedocs.io/en/latest/getting_started.html)
    2. [RTD :: Channels](https://channels.readthedocs.io/en/latest/introduction.html#turtles-all-the-way-down)
    3. [Python & Async Simplified](https://www.aeracode.org/2018/02/19/python-async-simplified/)
    4. My notes

        ```bash
        cd /Volumes/exFAT_Two/code_book/code_py_book_django2_by_example;
      
        grep -irnw Chapter_0*/*.md -e redis
        ```
    
- Pre-install

    1. Software

        ```bash
        brew update && brew install redis
        
        redis-server
        ```
    
    2. Packages

        ```bash
        pipenv install channels          # 
        pipenv install channels_redis    # a layer that uses Redis as its backing store
        ```
    
- Basic config

    ```python
    """ PROJECT/booktime/ :: routing.py """
    
    from channels.routing import ProtocolTypeRouter
    application = ProtocolTypeRouter({})


    """ PROJECT/booktime/ :: settings.py """

    INSTALLED_APPS = [
        "channels",     # must be put at the 1st (overriding `runserver`)
        ..
        ..
    ]

    # PROJ.FILENAME.CLASS_INST
    ASGI_APPLICATION = "booktime.routing.application"

    # Apparently, this one requires 
    #   two modules ->  channels, channels_redis
    #   app running ->  redis-server (brew install redis)
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            }
        }
    }


    # Now you can start the server as "usual"
    # || ./manage.py runserver
    # || Boom! The console produced something fun!!
    ```

### References
- I still don't really grasp the concept, here's the reading-list for myself.
    1. [Getting Started with Django Channels – Real Python](https://realpython.com/getting-started-with-django-channels/)
    2. [Channels Concepts — Channels 1.1.8 documentation](https://channels.readthedocs.io/en/1.x/concepts.html)
    3. [Understanding Django Channels · Arun Ravindran](https://arunrocks.com/understanding-django-channels/)
    4. [channels-example/show-notes.md at master · arocks/channels-example](https://github.com/arocks/channels-example/blob/master/show-notes.md)
- 