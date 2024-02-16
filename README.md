# PureThermal 3 Python Driver

## Overview
This simple Python driver is designed for the PureThermal 3 (PT3) - FLIR Lepton Smart I/O Module. It supports the visualization of thermal images in RGB and the publishing of MAX temperature data to an MQTT broker. The camera by default records 16bit greyscale images. Each individual pixel (160x120) corresponds to a temperature in kelvin with an advertised accuracy of +- 5 degrees. The `purethermal.py` script takes the image frame, packs it into a numpy array, and finds the max temperature value. That value is then converted to degrees celcius and broadcasted to an MQTT broker. If no broker is available it will contiously retry. The advertised max frame rate of the PT3 is 8.7 Hz.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/jakebonney10/purethermal3
   ```
3. Create virtual environment (if running on RPI)
   ```
   python3 -m venv myvenv
   source myvenv/bin/activate
   pip install --upgrade pip setuptools
   ```
4. Install dependencies (within venv if running on RPI):
   ```
   pip install opencv-python==4.90 paho-mqtt==1.6.1
   ```

## Usage

Run the `run_thermal_cam.sh` script to start capturing and publishing thermal camera data:

```
cd purethermal3
./run_thermal_cam.sh MQTT_HOST MQTT_PORT
```
or

```
python purethermal.py --host <MQTT_HOST> --port <MQTT_PORT>
```

For detailed usage and API documentation, refer to the [FLIR Lepton Documentation](https://www.flir.com/developer/lepton-integration/lepton-integration-windows/).

## Hardware Setup and Troubleshooting

- Ensure your PureThermal 3 module is correctly connected via USB-C or VIN.
- Blinky light will be solid while booting and will begin flashing during image capture.
- The lepton camera module makes a clicking noise when it performs its FFC (Full Frame Correction) every 3 minutes which is the default setting for the lepton. FLIR recommends not changing this to have the most accurate data. The FFC is visible in the received data as a short 5-10s 2-3 degree temperature spike. 
- The Lepton Camera module can pop out of the board. If PT3 board blinky light is on but no video this is most likely cause.
- FLIR has a [Windows application](https://flir.app.box.com/s/aos3khi6m2fkpxk3fsp7nfi3tdk3lra7) available for download. This works right out of the box to get images, upload firmware, check FFC settings, etc and is good for troubleshooting. Another option for linux is [GetThermal](https://github.com/groupgets/GetThermal) however it is no longer supported and buggy.
- If getting errors associated with 16bit greyscale and gstreamer video streaming check whether you have the right version of opencv installed.
  ```
  python3
  import cv2
  print(cv2.__version__)
  ```

## Firmware Flashing

Refer to the [PT3 Datasheet](https://groupgets-files.s3.amazonaws.com/PT3/PT3%20Datasheet%20Rev2%20Oct%202022.pdf) for instructions on flashing the firmware via USB or alternative methods.

## Future Development
- The basic openCV `imshow` command is resource intensive. Running on the RPI4 can cause it to freeze. Development of a less intensive flask app for video streaming over the network is the next development step. This line can be commented out of `purethermal.py` if we only care about MQTT data streaming.
- Segmenting the image to provide max temperature values within specified bounding boxes (monitoring individual NTCs)

## Support

For issues, questions, or contributions, please open an issue or pull request in the repository.

## License

This project is licensed under the APACHE2.0 License - see the LICENSE file for details.



