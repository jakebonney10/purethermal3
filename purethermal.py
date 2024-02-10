import cv2
import numpy as np

thermal_camera = cv2.VideoCapture(0)
thermal_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
thermal_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

# set up the thermal camera to get the gray16 stream and raw data
thermal_camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y','1','6',' '))
thermal_camera.set(cv2.CAP_PROP_CONVERT_RGB, 0)

def convert_temp_f(raw_temp):
    return (raw_temp / 100) * 9 / 5 - 459.67

while True:
    (grabbed, thermal_frame) = thermal_camera.read()

    max_temp = np.max(convert_temp_f(thermal_frame))
    min_temp = np.min(convert_temp_f(thermal_frame))
    print(f"Max Temp: {max_temp:.1f}F, Min Temp: {min_temp:.1f}F")

    # convert the gray16 image into a gray8
    cv2.normalize(thermal_frame, thermal_frame, 0, 255, cv2.NORM_MINMAX)
    thermal_frame = np.uint8(thermal_frame)
  
    # colorized the gray8 image using OpenCV colormaps
    thermal_frame = cv2.applyColorMap(thermal_frame, cv2.COLORMAP_INFERNO)
    cv2.imshow('gray8', thermal_frame)
    cv2.waitKey(1)

thermal_camera.release()
cv2.destroyAllWindows()
