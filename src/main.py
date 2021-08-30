#!/usr/bin/env python3

import logging
import os
import time

import paho.mqtt.client as mqtt
import uuid
import signal
from odometry import Odometry
from movement import Movement
from planet import Planet, Direction

client = None  # DO NOT EDIT


def run():
    # DO NOT CHANGE THESE VARIABLES
    #
    # The deploy-script uses the variable "client" to stop the mqtt-client after your program stops or crashes.
    # Your script isn't able to close the client after crashing.
    global client

    client_id = 'YOURGROUPID-' + str(uuid.uuid4())  # Replace YOURGROUPID with your group ID
    client = mqtt.Client(client_id=client_id,  # Unique Client-ID to recognize our program
                         clean_session=True,  # We want a clean session after disconnect or abort/crash
                         protocol=mqtt.MQTTv311  # Define MQTT protocol version
                         )
    log_file = os.path.realpath(__file__) + '/../../logs/project.log'
    logging.basicConfig(filename=log_file,  # Define log file
                        level=logging.DEBUG,  # Define default mode
                        format='%(asctime)s: %(message)s'  # Define default logging format
                        )
    logger = logging.getLogger('RoboLab')

    # THE EXECUTION OF ALL CODE SHALL BE STARTED FROM WITHIN THIS FUNCTION.
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER.

    print("-------------------- ROBOT --------------------")
    od = Odometry()
    mo = Movement()
<<<<<<< HEAD
    # mo.turn_90()
    # time.sleep(2)
    # mo.turn_360()
    # time.sleep(2)
    # mo.turn_45()
    test = mo.follow_line()
    od.calculate(test, 0, 0, Direction.NORTH)
=======
    mo.follow_line()
>>>>>>> 16fea2c90144e4718965eb40de5046246e3298ff
    print("-----------------------------------------------")


# DO NOT EDIT
def signal_handler(sig=None, frame=None, raise_interrupt=True):
    if client and client.is_connected():
        client.disconnect()
    if raise_interrupt:
        raise KeyboardInterrupt()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    try:
        run()
        signal_handler(raise_interrupt=False)
    except Exception as e:
        signal_handler(raise_interrupt=False)
        raise e
