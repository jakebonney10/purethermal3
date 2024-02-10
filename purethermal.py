import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time

# Setup MQTT client
client = mqtt.Client()
MQTT_HOST = "localhost"
MQTT_PORT = 1883

def try_mqtt_connect():
    try:
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        return True
    except Exception as e:
        print(f"MQTT connection error: {e}")
        return False

mqtt_connected = try_mqtt_connect()

try:
    thermal_camera = cv2.VideoCapture(0)
    thermal_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
    thermal_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
    thermal_camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y','1','6',' '))
    thermal_camera.set(cv2.CAP_PROP_CONVERT_RGB, 0)

    def convert_temp_f(raw_temp):
        return (raw_temp / 100) * 9 / 5 - 459.67

    while True:

        if not mqtt_connected:
            mqtt_connected = try_mqtt_connect()

        (grabbed, thermal_frame) = thermal_camera.read()

        max_temp = np.max(convert_temp_f(thermal_frame))
        min_temp = np.min(convert_temp_f(thermal_frame))
        print(f"Max Temp: {max_temp:.1f}F, Min Temp: {min_temp:.1f}F")

        if mqtt_connected:
            try:
                client.publish("temp_max", f"{max_temp:.1f}")
            except Exception as e:
                print(f"Failed to publish: {e}")
                mqtt_connected = False  # Assume disconnection on failure

        cv2.normalize(thermal_frame, thermal_frame, 0, 255, cv2.NORM_MINMAX)
        thermal_frame = np.uint8(thermal_frame)
        thermal_frame = cv2.applyColorMap(thermal_frame, cv2.COLORMAP_INFERNO)
        cv2.imshow('gray8', thermal_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Interrupted")
finally:
    thermal_camera.release()
    cv2.destroyAllWindows()
