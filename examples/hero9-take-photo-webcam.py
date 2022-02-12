import sys
import time
from goprocam import GoProCamera, constants, exceptions
import threading
from signal import signal, SIGINT

isOpenGoPro = True


def take_photo(interface):
    gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP(
        interface), camera=constants.gpcontrol, webcam_device=interface, api_type=constants.ApiServerType.OPENGOPRO if isOpenGoPro else constants.ApiServerType.SMARTY)
    try:
        r = gopro.setWiredControl(constants.on)
        print(r)
    except exceptions.WiredControlAlreadyEstablished:
        pass  # sometimes throws 500 server error when camera is already on wired control mode

    while True:
        gopro.take_photo()
        time.sleep(2)
        print("Photo taken")
        exit()


def handler(s, f):
    thr.stop()
    quit()


signal(SIGINT, handler)

cameras = sys.argv[1]
cameras = cameras.split(",")

for interface in cameras:
    thr = threading.Thread(target=take_photo, args=(interface,))
    thr.start()
