import logging
import aioredis

from django.shortcuts import get_object_or_404

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import models

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    About the superclass
        [My understanding]
            It automatically JSON-encodes/decodes msgs as they come in & go out.
            And we'll need to implement the respective methods (recei.., conn.., disco..).

        [Notes from book]
            It takes care of the <WebSocket low-level aspects> and JSON encoding (nice).

    Every consumer (thus the classes in this file)
    will receive a `scope` object after the class is initialized.

        scope['path']       the path of the request
        scope['user']       the current user  ( when the auth is enabled )
        scope['url_route']  the matched route ( if using a `URLRouter`   )

    # TODO
        Right now, I've understood most of the concepts of channels,
        well, not of all of them, especially the `group_add` (not new, but ah).

    Finally
        Manually testing by accessing 'http://localhost:8000/customer-service/3/' (yay).
            Open two browser tabs,
            you should be able to see each other's msg if you're in the same room.

        BUT, there are (ALREADY FIXED!!) errors in the console (403Error)
        Well, the origin of this bug is STILL a typo done by myself...

        Just so you know where it is

            ORIGINAL        if cont_type == "message":
                                await self.channel_layer.group_add()

            SHOULD BE       if cont_type == "message":
                                await self.channel_layer.group_send()
    """

    EMPLOYEE = 2
    CLIENT = 1

    @staticmethod
    def get_user_type(user, order_id):
        """
        This one is quite simple though..
        You <identify the user type>, then use it inside the other methods.

        Do note that the usage down below will be like
        >> something["user"]    // what I want to say is that
        >> something["order"]   // it'll used like an dict["key"] kind of thing
        """

        order = get_object_or_404(models.Order, pk=order_id)

        # Two scenarios here
        #   1. If 'employee', assign the user he's talking to the Orders
        #   2. If not (user), simply return the user (as a CLIENT)
        if user.is_employee:
            order.last_spoken_to = user
            order.save()

            return ChatConsumer.EMPLOYEE

        elif order.user == user:
            return ChatConsumer.CLIENT
        else:
            return None

    async def connect(self):
        """
        Partly, we're defining a simple format for <WebSocket messages>.
        In another word, this is also the "protocol" (as the author said so).

            SERVER to CLIENT
            {
                type      : "TYPE",
                username  : "WHO is the ORIGINATOR of the event",
                message   : "THE displayed MESSAGE" (optional?)
            }

            CLIENT to SERVER
            {
                type      : "TYPE",
                message   : "THE displayed MESSAGE" (optional?)
            }

            About the values for the key 'type'

                1. Server to Client
                    chat_join       : "The username JOINed the chat"
                    chat_leave      : "The username LEFT   the chat"
                    chat_message    : "The username SENT   a message"

                2. Client to Server
                    message         : "The username SENT   a message"
                    heartbeat       : "A ping to let server KNOW the user is ACTIVE"


        Also, lemme break this function down a little bit.
        -- get order_id & use it in room_name
        -- anonymous yo? fuck off
        -- get the user type (access by 'wrapping-async-consumer-in-sync-function)
        -- toggling the value of `authorized` based on the user type
        -- do some Redis operations if authorized (init & add->accept->send)
        """

        # ----- get the order id from `self.scope` & use it in room_name -----

        self.order_id = self.scope["url_route"]["kwargs"][
            "order_id"
        ]
        self.room_group_name = ("customer-service_%s" % self.order_id)

        # ----- initialize a variable for later uses   -----

        authorized = False

        # ----- Fuck off if the user is (not even) UN-authorized -----

        if self.scope["user"].is_anonymous:
            await self.close()

        # ----- Get the bloody user type (access by 'wrapping-async-consumer-in-sync-function)-----

        user_type = await database_sync_to_async(
            self.get_user_type
        )(self.scope["user"], self.order_id)

        # ----- Toggling the value of `authorized` based on user_type -----

        if user_type == ChatConsumer.EMPLOYEE:
            logger.info(
                "Opening chat stream for employee %s",
                self.scope["user"],
            )

            authorized = True

        elif user_type == ChatConsumer.CLIENT:
            logger.info(
                "Opening chat stream for client %s",
                self.scope["user"],
            )

            authorized = True

        else:
            logger.info(
                "Unauthorized connection from %s",
                self.scope["user"],
            )

            await self.close()

        if authorized:
            # Just so you know (for the unconscious self)
            # the code down below are doing DB operations (Redis, of course).

            self.redis_conn = await aioredis.create_redis(
                "redis://localhost"
            )

            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )

            await self.accept()

            # As the author says,
            # -- the `group_send` is NOT sending the data back to the browser's WS conn.
            # -- It's only used to << relay info btwn consumers >> using conf_ed channel layer.
            # -- Each consumer'll receive this data through message handlers (the `chat_xxx`).
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_join",
                    "username": self.scope["user"].get_full_name(),
                },
            )

    async def disconnect(self, close_code):
        if not self.scope["user"].is_anonymous:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_leave",
                    "username": self.scope["user"].get_full_name(),
                },
            )

            logger.info(
                "Closing chat stream for user %s",
                self.scope["user"],
            )

            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive_json(self, content, **kwargs):
        """
        From my understanding so far, this method does
        messaging jobs about <Client to Server> (quite obvious though).
        """

        cont_type = content.get("type")

        if cont_type == "message":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "username": self.scope["user"].get_full_name(),
                    "message": content["message"],
                }
            )

        # This type is used to
        #   send a ping to the server -> let them know "I'm NOT dead!!"
        elif cont_type == "heartbeat":

            # For any user, whether a cust-service repres OR an end-user
            # the ws-conn will become unavailable
            # -- once all WebSocket connections init_ed by them are closed
            # -- or become inactive for than 10 seconds (way to handle net-prob & brow-crash).

            # For the 2nd one, we'll rely on the feature provided by Redis.
            await self.redis_conn.setex(
                "%s_%s" % (
                    self.room_group_name,
                    self.scope["user"].email,
                ),
                10,  # expiration (setex => set expiration time, yay!)
                "1"  # ? dummy value
            )

    # For these three methods (aka. 'Handlers', it DOES send the msg BACK to the browser.
    #   Why? Because ALL the processing will happen in the frontend (go check the HTML!).

    async def chat_message(self, event):
        await self.send_json(event)

    async def chat_join(self, event):
        await self.send_json(event)

    async def chat_leave(self, event):
        await self.send_json(event)
