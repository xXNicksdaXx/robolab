#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import platform
import ssl
import paho.mqtt.client as mqtt

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

# Callback function for receiving messages
def on_message(client, data, message):
    print('Got message with topic "{}":'.format(message.topic))
    data = json.loads(message.payload.decode('utf-8'))
    print(json.dumps(data, indent=2))
    print("\n")


# Basic configuration of MQTT
client = mqtt.Client(client_id="<GROUP>", clean_session=False, protocol=mqtt.MQTTv31)

client.on_message = on_message_excepthandler # Assign pre-defined callback function to MQTT client
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.username_pw_set('<GROUP>', password='<PASS>') # Your group credentials
client.connect('mothership.inf.tu-dresden.de', port=8883)
client.subscribe('explorer/<GROUP>', qos=1) # Subscribe to topic explorer/xxx

# Start listening to incoming messages
client.loop_start()

while True:
	input('Press Enter to continue...\n')

client.loop_stop()
client.disconnect()

# Fix: SSL certificate problem on macOS
if all(platform.mac_ver()):
    from OpenSSL import SSL


class Communication:
    """
    Class to hold the MQTT client communication
    Feel free to add functions and update the constructor to satisfy your requirements and
    thereby solve the task according to the specifications
    """

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

        self.logger = logger

    # DO NOT EDIT THE METHOD SIGNATURE
    def on_message(self, client, data, message):
        """
        Handles the callback if any message arrived
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        payload = json.loads(message.payload.decode('utf-8'))
        self.logger.debug(json.dumps(payload, indent=2))

        # YOUR CODE FOLLOWS (remove pass, please!)
        pass

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
        pass

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
