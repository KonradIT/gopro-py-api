import sys
import time
from goprocam import GoProCamera, constants
import threading


def take_photo(interface):
    gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP(
        interface), camera=constants.gpcontrol, webcam_device=interface)
    while True:
        gopro.take_photo()
        time.sleep(2)
        print("Photo taken")


cameras = sys.argv[1]
cameras = cameras.split(",")

for interface in cameras:
    thr = threading.Thread(target=take_photo, args=(interface,))
    thr.start()
