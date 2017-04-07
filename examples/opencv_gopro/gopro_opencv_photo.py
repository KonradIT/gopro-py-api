import cv2
import numpy as np
from goprocam import GoProCamera
from goprocam import constants
import urllib.request
cascPath="/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
eyePath="/usr/share/opencv/haarcascades/haarcascade_eye.xml"
eye_cascade = cv2.CascadeClassifier(eyePath)
face_cascade = cv2.CascadeClassifier(cascPath)
gpCam = GoProCamera.GoPro()
gpCam.gpControlSet(constants.Photo.RESOLUTION, constants.Photo.Resolution.R12W)
photo_url = gpCam.take_photo(5)
url = urllib.request.urlopen(photo_url)
photo = np.array(bytearray(url.read()), dtype=np.uint8)
img= cv2.imdecode(photo, -1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()