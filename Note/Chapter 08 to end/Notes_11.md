### Foreword
- Starting from this chapter, we'll build something more *complicated*.
    - Such as these topics
        - Redis
        - WebSocket
        - Django *Channels*
- About *Django Channels*
        
    > *Channels* allows us to write **asynchronous** code to deal with incoming requests,<br>
    > &nbsp;&nbsp;which is helpful is case we have a naturall async interaction between C|S, e.g. A *chat session*
    
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
    
- Pre-conf

    