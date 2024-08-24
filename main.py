from javascript import require, On, Once, AsyncTask, once, off
from random import randint
import time
import re

# Import the javascript libraries
mineflayer = require("mineflayer")

# Global bot parameters
server_host = "bluek1d.aternos.me"
server_port = 15161
reconnect = True
version = "1.19.4"


class MCBot:

    def __init__(self, bot_name):
        self.bot_args = {
            "host": server_host,
            "port": server_port,
            "username": bot_name,
            "version": version,
            "hideErrors": False,
        }
        self.reconnect = reconnect
        self.bot_name = bot_name
        self.start_bot()

    # Tags bot username before console messages
    def log(self, message):
        print(f"[{self.bot.username}] {message}")

    # Start mineflayer bot
    def start_bot(self):
        self.bot = mineflayer.createBot(self.bot_args)

        self.start_events()

    # Attach mineflayer events to bot
    def start_events(self):

        # Login event: Triggers on bot login
        @On(self.bot, "login")
        def login(this):

            # Displays which server you are currently connected to
            self.bot_socket = self.bot._client.socket
            self.log(
                f"Logged in to {self.bot_socket.server if self.bot_socket.server else self.bot_socket._host }"
            )

        # Kicked event: Triggers on kick from server
        @On(self.bot, "kicked")
        def kicked(this, reason, loggedIn):
            if loggedIn:
                self.log(f"Kicked whilst trying to connect: {reason}")

        # Chat event: Triggers on chat message
        @On(self.bot, "messagestr")
        def messagestr(this, message, messagePosition, jsonMsg, sender, verified=None):
            if messagePosition == "chat":
                self.log(message)
                if "?end" in message:
                    self.bot.chat("/home")
                    self.bot.chat(">Estoy en el end!")
                elif "?tira una moneda" in message:
                    if randint(1, 2) == 1:
                        self.bot.chat("¡Cara!")
                    else:
                        self.bot.chat("¡Cruz!")
                elif "?tirar un dado" in message:
                    self.bot.chat(f"Sacaste un {randint(1, 6)}")
                elif "?tpa" in message:
                    self.bot.chat("/tpaccept")

                elif "?decir" in message:
                    # Elimina '?decir ' del inicio del mensaje
                    decir_message = message.replace("<bluek1d> ?decir ", "", 1)
                    self.bot.chat(decir_message)
            elif messagePosition == "system":
                if "has sent you a teleport request" in message:
                    self.bot.chat("/tpaccept")

        # End event: Triggers on disconnect from server
        @On(self.bot, "end")
        def end(this, reason):
            self.log(f"Disconnected: {reason}")

            # Turn off old events
            off(self.bot, "login", login)
            off(self.bot, "kicked", kicked)
            off(self.bot, "messagestr", messagestr)
            # Reconnect
            if self.reconnect:
                self.log(f"Attempting to reconnect")
                self.start_bot()

            # Last event listener
            off(self.bot, "end", end)


# Run function that starts the bot(s)
bot = MCBot("xanarkyBOT")
