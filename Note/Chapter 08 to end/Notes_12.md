### Foreword
- This file starts from **page 303** <small>(real)</small>.
    - We'll BUILD a *Chat Dashboard* 
        1. Let the *customer-service represt* able to **see if  there're customers waiting to be served**.
        2. The dashboard'd **dynamically update** with a *list of chat     rooms* & the *various people in it*.
    - We'll ADOPT a new approach *HTTP Server-sent Events* <small>( **unidirectional**, simpler than *WS* )</small>
        - It is *an HTTP connection* that **stays open** & **keeps receiving** *chunks of information*.
        - Every *chunks of information* is **prefixed** with ```"data:"```
        - Every *chunks of information* is **terminated** with *two newline characters*
   
-----

### References
- Concepts
    1. [WebSockets vs. Server-Sent events/EventSource](https://stackoverflow.com/questions/5195452/websockets-vs-server-sent-events-eventsource)
- Concepts with usage
    1. [Server-Sent Events explained with usecases](https://streamdata.io/blog/server-sent-events/)