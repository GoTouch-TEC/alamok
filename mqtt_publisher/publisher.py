import os
import paho.mqtt.client as mqtt
import json
import time


class Publisher ():

    def __init__(self, broker_address, broker_port=1883, out_topic="", in_topic="", username="", password="", device_id="", on_publish=None):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.out_topic = out_topic
        self.in_topic = in_topic
        self.device_id = device_id
        if(self.device_id):
            self.client = mqtt.Client(self.device_id)
        else:
            self.client = mqtt.Client()
        if(self.username):
            self.client.username_pw_set(self.username, password=self.password)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        if(on_publish is not None):
            self.client.on_publish = on_publish

    def start(self):
        self.debug("connecting to broker")
        try:
            self.client.connect_async(
                self.broker_address, port=self.broker_port)
            self.client.loop_start()
        except Exception as error:
            self.debug("Failed connection")
            self.debug(error)

    def on_message(self, client, userdata, message):
        self.debug('\n')
        self.debug("message received ", str(message.payload.decode("utf-8")))
        self.debug("message topic=", message.topic)
        self.debug("message qos=", message.qos)
        self.debug("message retain flag=", message.retain)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.debug("Connected to broker")
        else:
            self.debug("Connection failed")

    def publish_data(self, data):
        try:
            msg_info = self.client.publish(self.out_topic, data, qos=1)
            self.debug("Published:", data)
            return msg_info.mid
        except Exception:
            self.debug("Error publishing")

    def on_disconnect(self, client, userdata, rc):
        if(rc != 0):
            self.debug("Unexpected disconnection.")

    def stop(self):
        self.debug("disconnect...mqtt")
        try:
            self.client.disconnect()
            self.debug('disconnected...mqtt')
            self.client.loop_stop()
        except Exception:
            self.debug("Error disconnecting client")

    def status(self):
        state = False
        if(self.client._state == 1):
            state = True
        return state

    def debug(self, *params):
        if(__debug__):
            for param in params:
                print(param, end=' ')
            print("")
