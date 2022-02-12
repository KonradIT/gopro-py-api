import sys
import time
from goprocam import GoProCamera, constants
import threading
from signal import signal, SIGINT


def record_video(interface: str) -> None:

    gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP(
        interface), camera=constants.gpcontrol, webcam_device=interface, api_type=constants.ApiServerType.OPENGOPRO)
    try:
        r = gopro.setWiredControl(constants.on)
        gopro.checkResponse(r)
    except:
        pass  # sometimes throws 500 server error when camera is already on wired control mode

    r = gopro.shoot_video(10)
    print(r)
    print("Video recorded")
    exit()


def handler(s, f):
    thr.stop()
    quit()


signal(SIGINT, handler)

cameras = sys.argv[1]
cameras = cameras.split(",")

for interface in cameras:
    thr = threading.Thread(target=record_video, args=(interface,))
    thr.start()
