#!/bin/python3
import datetime
import json
import paho.mqtt.client
import queue
import struct

class Monitor():
    def __init__(self):
        self.hostname = "192.168.1.17"
        self.port = 1883
        self.bindings = {}
        self.q = queue.Queue()
        self.topics = set()
        self.connected = False

    def on(self, topic, f): # Only takes full literal topics, ones like a/#/b will fail
        self.topics.add(topic)
        if self.connected:
            self.client.subscribe(topic)

        if topic not in self.bindings:
            self.bindings[topic] = []
        self.bindings[topic].append(f)

    def start(self):
        self.client = paho.mqtt.client.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.connect(self.hostname, self.port)

    def on_connect(self, client, _, connect_flags, properties):
        for topic in self.topics:
            self.client.subscribe(topic)
        self.connected = True

    def wait(self):
        self.client.loop_forever()

    def on_message(self, client, _, message):
        callbacks = self.bindings.get(message.topic, [])
        #print("{}: {}".format(message.topic, repr(callbacks)))
        for callback in callbacks:
            callback(client, message)

def control_blinds(client, message):
    j = json.loads(message.payload)
    state = j["action"]
    for blind, level in { 1: 28, 2: 25, 3: 25, }.items():
        if state == "open":
            topic, message = "zigbee2mqtt/Blinds/{}/Blind/set".format(blind), '{"state": "OPEN" }'
        elif state == "close":
            topic, message = "zigbee2mqtt/Blinds/{}/Blind/set".format(blind), '{{"position": {} }}'.format(level)
        client.publish(topic, message)

if __name__ == '__main__':
    m = Monitor()
    m.start()

    m.on("zigbee2mqtt/Blinds/1/Remote", control_blinds)
    m.wait()
