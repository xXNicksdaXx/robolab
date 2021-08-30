#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import platform
import ssl
import paho.mqtt.client as mqtt
from queue import Queue

# Fix: SSL certificate problem on macOS
if all(platform.mac_ver()):
    from OpenSSL import SSL

class Communication:
    """
    Class to hold the MQTT client communication
    Feel free to add functions and update the constructor to satisfy your requirements and
    thereby solve the task according to the specifications
    """
    planetsub = None
    q = Queue()

    # this is a helper method that catches errors and prints them
    # it is necessary because on_message is called by paho-mqtt in a different thread and exceptions
    # are not handled in that thread
    #
    # you don't need to change this method at all
    def on_message_excepthandler(client, data, message):
        try:
            on_message(client, data, message)
        except:
            import traceback
            traceback.print_exc()
            raise


    def __init__(self, mqtt_client, logger):
        """
        Initializes communication module, connect to server, subscribe, etc.
        :param mqtt_client: paho.mqtt.client.Client
        :param logger: logging.Logger
        """
        # DO NOT CHANGE THE SETUP HERE
        self.client = mqtt_client
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)
        self.client.on_message = self.safe_on_message_handler
        # Add your client setup here
        self.client = mqtt.Client(client_id="MQTT_FX_Client", clean_session=False, protocol=mqtt.MQTTv31)

        self.client.username_pw_set('125', password='IWDwkt9Ao3')  # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.client.subscribe('explorer/125', qos=1)  # Subscribe to topic explorer/xxx

        self.logger = logger

    # Start listening to incoming messages
    client.loop_start()

    while True:
        input('Press Enter to continue...\n')

    client.loop_stop()
    client.disconnect()

    # DO NOT EDIT THE METHOD SIGNATURE
    def on_message(self, client, data, message):
        """
        Handles the callback if any message arrived
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        payload = json.loads(message.payload.decode('utf-8'))  # str -> dict
        self.logger.debug(json.dumps(payload, indent=2))

        # YOUR CODE FOLLOWS (remove pass, please!)
        info = payload["payload"]
        if payload["from"] == "server":
            targets = {
                "planet": ((info["startX"], info["startY"]), info["startOrientation"]),
                "path": (((info["endX"], info["endY"]), info["endDirection"]), info["pathWeight"]),
                "pathSelect": info["startDirection"],
                "pathUnveiled": (
                    ((info["startX"], info["startY"]), info["startDirection"]),
                    ((info["endX"], info["endY"]), info["endDirection"]),
                    info["pathWeight"]
                ),
                "target": (info["targetX"], info["targetY"])
            }
            if payload["type"] == "planet":
                self.planetsub = "planet/" + info["planetName"] + "/125"
                self.client.subscribe(self.planetsub)

            if payload['type'] in targets:
                self.q.put(targets[payload['type']])

    # DO NOT EDIT THE METHOD SIGNATURE
    #
    # In order to keep the logging working you must provide a topic string and
    # an already encoded JSON-Object as message.
    def send_message(self, topic, message):
        """
        Sends given message to specified channel
        :param topic: String
        :param message: Object
        :return: void
        """
        self.logger.debug('Send to: ' + topic)
        self.logger.debug(json.dumps(message, indent=2))

        # YOUR CODE FOLLOWS (remove pass, please!)
        self.client.publish(topic, json.dumps(message), qos=1)

    # DO NOT EDIT THE METHOD SIGNATURE OR BODY
    #
    # This helper method encapsulated the original "on_message" method and handles
    # exceptions thrown by threads spawned by "paho-mqtt"
    def safe_on_message_handler(self, client, data, message):
        """
        Handle exceptions thrown by the paho library
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        try:
            self.on_message(client, data, message)
        except:
            import traceback
            traceback.print_exc()
            raise

    def send_ready(self):
        """
        Send message of the type "ready"
        :return: void
        """
        sdmessage = {"from": "client", "type": "ready"}
        self.send_message("explorer/125", sdmessage)

    def send_path(self, startX, startY, startD, endX, endY, endD, pathStatus):
        """
        Send message of the type "path"
        :param startX: integer
        :param startY: integer
        :param startD: integer
        :param endX: integer
        :param endY: integer
        :param endD: integer
        :param pathStatus: String free|blocked
        :return: void
        """
        sdmessage = {"from": "client", "type": "path",
                    "payload": {"startX": startX, "startY": startY, "startDirection": startD, "endX": endX,
                                "endY": endY, "endDirection": endD, "pathStatus": pathStatus}}
        self.send_message(self.planetsub, sdmessage)

    def send_path_invalid(self, startX, startY, startD, endXc, endYc, endDc, pathStatus):
        """
               Send message of the type "path"
               :param startX: integer
               :param startY: integer
               :param startD: integer
               :param endXc: integer
               :param endYc: integer
               :param endDc: integer
               :param pathStatus: String free|blocked
               :return: void
               """
        sdmessage = {"from": "client", "type": "path",
                     "payload": {"startX": startX, "startY": startY, "startDirection": startD, "endXc": endXc,
                                 "endYc": endYc, "endDirection": endDc, "pathStatus": pathStatus}}
        self.send_message(self.planetsub, sdmessage)

