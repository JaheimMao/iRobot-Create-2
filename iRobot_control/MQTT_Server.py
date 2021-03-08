import json

import paho.mqtt.client as mqtt

import iRobot_server

HOST = "182.92.194.252"
Port = 1883


def on_connect(client, userdata, flags, rc):
    print("connection with result code " + str(rc))
    client.subscribe("command")


def on_message(client, userdata, msg):
    jsonObject = json.loads(msg.payload)
    command = jsonObject["command"]

    if command == "forward":
        print(command)
        iRobot_server.create_go(iRobot_server.bot)
    elif command == "back":
        iRobot_server.create_back(iRobot_server.bot)
        print(command)
    elif command == "right":
        print(command)
        iRobot_server.create_right(iRobot_server.bot)
    elif command == "left":
        print(command)
        iRobot_server.create_left(iRobot_server.bot)
    elif command == "clean":
        print(command)
        iRobot_server.create_clean(iRobot_server.bot)
    elif command == "spot":
        print(command)
        iRobot_server.create_spot(iRobot_server.bot)


def on_service(client):
    client.username_pw_set("admin", "public")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOST, Port, 60)

    client.loop_start()

