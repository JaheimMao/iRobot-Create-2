import paho.mqtt.client as mqtt
import json

import MQTT_Server
import iRobot_server


def main():
    iRobot_server.create_start(iRobot_server.bot)
    client = mqtt.Client("irobot")
    MQTT_Server.on_service(client)
    location_x_old = 0
    location_y_old = 0
    voltage_old = 0
    current_old = 0
    velocity_old = 0
    angle_now = 0

    while True:
        encoder_counts_left_old, encoder_counts_right_old = iRobot_server.get_encoder_counts(iRobot_server.bot)
        voltage_new = iRobot_server.get_voltage(iRobot_server.bot)
        current_new = iRobot_server.get_current(iRobot_server.bot)
        velocity_new = iRobot_server.get_velocity(iRobot_server.bot)

        if voltage_new != voltage_old or current_new != current_old or velocity_new != velocity_old:
            status_string = {"function": "data", "current": str(current_new), "voltage": str(voltage_new),
                             "velocity": str(velocity_new)}
            print(status_string)

            status_json = json.dumps(status_string)
            client.publish("irobot", status_json)

            voltage_old = voltage_new
            current_old = current_new
            velocity_old = velocity_new

        encoder_counts_left_new, encoder_counts_right_new = iRobot_server.get_encoder_counts(iRobot_server.bot)

        distance = iRobot_server.calculate_distance(encoder_counts_left_old, encoder_counts_left_new,
                                                    encoder_counts_right_old, encoder_counts_right_new)

        angle = iRobot_server.get_angle(encoder_counts_left_old, encoder_counts_left_new,
                                        encoder_counts_right_old, encoder_counts_right_new)

        if angle > 0.1:
            print(angle)
            angle_now = angle + angle_now

        if distance > 0.1:
            print(distance)
            print(str(encoder_counts_right_old) + " " + str(encoder_counts_right_new))
            print(str(encoder_counts_left_old) + " " + str(encoder_counts_left_new))

            location_x_new, location_y_new = iRobot_server.get_location(location_x_old, location_y_old,
                                                                        distance, angle_now)

            location_string = {"function": "location", "x1": str(int(location_x_old)), "y1": str(int(location_y_old)),
                               "x2": str(int(location_x_new)), "y2": str(int(location_y_new))}
            print(location_string)

            location_json = json.dumps(location_string)
            client.publish("irobot", location_json)
            location_x_old = location_x_new
            location_y_old = location_y_new


if __name__ == '__main__':
    main()
