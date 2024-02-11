import cv2
import numpy as np
import paho.mqtt.client as mqtt
import argparse
from flask import Flask, Response

class ThermalCamera:
    def __init__(self, mqtt_host, mqtt_port):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client()
        self.thermal_camera = cv2.VideoCapture(0)
        self.configure_camera()
        self.mqtt_connected = self.try_mqtt_connect()

        app = Flask(__name__)

    def generate_frames(self):
        ret, buffer = cv2.imencode('.jpg', self.thermal_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
    @app.route('/video')
    def video():
        return Response(self.generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    def configure_camera(self):
        self.thermal_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        self.thermal_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        self.thermal_camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y','1','6',' '))
        self.thermal_camera.set(cv2.CAP_PROP_CONVERT_RGB, 0)

    def try_mqtt_connect(self):
        try:
            self.client.connect(self.mqtt_host, self.mqtt_port, 60)
            return True
        except Exception as e:
            print(f"MQTT connection error: {e}")
            return False

    @staticmethod
    def convert_temp_c(raw_temp):
        return (raw_temp / 100) - 273.15

    def run(self):
        try:
            while True:
                if not self.mqtt_connected:
                    self.mqtt_connected = self.try_mqtt_connect()

                grabbed, thermal_frame = self.thermal_camera.read()

                max_temp = np.max(self.convert_temp_c(thermal_frame))
                min_temp = np.min(self.convert_temp_c(thermal_frame))
                print(f"Max Temp: {max_temp:.1f}C, Min Temp: {min_temp:.1f}C")

                if self.mqtt_connected:
                    try:
                        self.client.publish("thermal_camera/temp_max", f"{max_temp:.1f}")
                    except Exception as e:
                        print(f"Failed to publish: {e}")
                        self.mqtt_connected = False

                cv2.normalize(thermal_frame, thermal_frame, 0, 255, cv2.NORM_MINMAX)
                thermal_frame = np.uint8(thermal_frame)
                thermal_frame = cv2.applyColorMap(thermal_frame, cv2.COLORMAP_INFERNO)
                cv2.imshow('gray8', thermal_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            print("Interrupted")
        finally:
            self.thermal_camera.release()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run thermal camera script with MQTT host specification.')
    parser.add_argument('--host', type=str, default='localhost', help='MQTT host address')
    parser.add_argument('--port', type=int, default=1883, help='MQTT host port')
    args = parser.parse_args()
    print(f"MQTT Host: {args.host}, Port: {args.port}")

    thermal_cam = ThermalCamera(args.host, args.port)
    thermal_cam.run()
    thermal_cam.app.run(debug=True, threaded=True)
