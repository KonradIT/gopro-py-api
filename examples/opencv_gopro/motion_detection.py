import cv2                            # importing Python OpenCV
from datetime import datetime         # importing datetime for naming files w/ timestamp
import socket
from goprocam import GoProCamera
from goprocam import constants
from time import time
import argparse

gpCam = GoProCamera.GoPro()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gp_sync_time=time()
gpCam.livestream("start")

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--save_photo", action='store_true', help="Screenshot from opencv")
ap.add_argument("-p", "--take_photo", action='store_true', help="Take photos every time there is movement in the frame")
ap.add_argument("-r", "--record", action='store_true', help="Start recording after the first movement")
ap.add_argument("-t", "--tag", action='store_true', help="Hilight Tag on movements when recording")
ap.add_argument("-u", "--uri", help="Source URL")
args = ap.parse_args()
def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)
window = "GoPro View"
threshold = 81500
source = "udp://127.0.0.1:10000"
if args.uri != None:
  print(args.uri)
  source = args.uri
cam = cv2.VideoCapture(source)
cv2.namedWindow(window)

t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
timeCheck = datetime.now().strftime('%Ss')

def release():
  cv2.destroyAllWindows()
  cam.release()
  gpCam.shutter(constants.stop)
if args.take_photo:
  gpCam.shutter("stop")
  gpCam.mode(constants.Mode.PhotoMode, constants.Mode.SubMode.Photo.Single_H5)
while True:
  cv2.imshow(window, cam.read()[1] )
  if cv2.countNonZero(diffImg(t_minus, t, t_plus)) > threshold and timeCheck != datetime.now().strftime('%Ss'):
    dimg= cam.read()[1]
    print(datetime.now(), "Movement detected")
    if args.save_photo:
      cv2.imwrite(datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg', dimg)
    if args.take_photo:
      gpCam.shutter("stop")
      gpCam.take_photo()
    if args.record:
      if gpCam.IsRecording() == 0:
        gpCam.shoot_video()
    if args.record == True and args.tag == True:
      gpCam.hilight()
  timeCheck = datetime.now().strftime('%Ss')
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
  if time() - gp_sync_time >= 2.5:
    sock.sendto("_GPHD_:0:0:2:0.000000\n".encode(), ("10.5.5.9", 8554))
    gp_sync_time=time()

  key = cv2.waitKey(1) & 0xFF
  if key == ord("q"):
    release()
    break
release()
