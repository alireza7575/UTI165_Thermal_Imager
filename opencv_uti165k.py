import numpy as np
import time
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages') # in order to import cv2 under python3
import cv2

sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages') # append back in order to import rospy

import struct

camera_num = 0

	

# Parameter specifying how much the image size is reduced at each image scale.
fd_scaleFactor  = 1.1 
 
# Parameter specifying how many neighbors each candidate rectangle should have to retain it.
fd_minNeighbors  = 3 




for camera_num in range(6):
    cam = cv2.VideoCapture(camera_num)
    if not cam.isOpened():
        print("Was not able to open camera", camera_num)
        cam.release()
        continue
    if not cam.set(3, 240):
        print("Was not able to set camera", camera_num, "width to 240 pixels")
        cam.release()
        continue
    if not cam.set(4, 321):
        print("Was not able to set camera", camera_num, "height to 321 pixels")
        cam.release()
        continue
    if cam.get(3) != 240:
        print("Was not able to set camera", camera_num, "width to 240 pixels")
        cam.release()
        continue
    break

print("Camera %d open at size: (%d x %d) %d FPS" % (camera_num, cam.get(3), cam.get(4), cam.get(5)))

cv2.namedWindow('Thermal Camera - Press Q to quit', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Thermal Camera - Press Q to quit', 480, 642)

while(True):
    # Capture frame-by-frame
    ret, frame = cam.read()

    if not ret:
        print("Failed to fetch frame")
        time.sleep(0.1)
        continue
    #print("Frame OK!")
    colorframe = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    
 
# Initializes classifiers
    face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')

    # detectMultiScale requires an CV_U8 image (gray).

    # Detects objects of different sizes in the input image. 
    # The detected objects are returned as a list of rectangles.
    image_faces = face_cascade.detectMultiScale(gray_image, fd_scaleFactor, fd_minNeighbors, minSize=(80, 80))
    
    # detect eyes for each face.
    for (x, y, w, h) in image_faces:
        cv2.rectangle(colorframe, (x, y), (x+w, y+h), (0, 255, 0), 2)

    
    # Display the resulting frame
    cv2.imshow('Thermal Camera - Press Q to quit', colorframe)

    cam.set(cv2.CAP_PROP_CONVERT_RGB, 0)
    ret, frame = cam.read()
    if not ret:
        print("Failed to fetch frame")
        time.sleep(0.1)
        continue

    print("Temp calculation (experimental): " )
    temp = struct.unpack("h", frame[320][0][0:2])[0]/10


    print(temp)
    if temp > 40:
        print("high")
    
    cam.set(cv2.CAP_PROP_CONVERT_RGB, 1)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #yuvframe = cv2.cvtColor(frame, cv2.COLOR_RGB2YUV)
    #print(yuvframe[-1][0:3])
cam.release()
cv2.destroyAllWindows()
