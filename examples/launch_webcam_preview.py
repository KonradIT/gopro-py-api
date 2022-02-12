from signal import signal, SIGINT
from goprocam import GoProCamera, constants
import sys

gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP(
    sys.argv[1]), camera=constants.gpcontrol, webcam_device=sys.argv[1])


def handler(s, f):
    gopro.stopWebcam()
    quit()


signal(SIGINT, handler)

try:
    gopro.setWiredControl(constants.off)
except:
    pass
gopro.startWebcam(constants.Webcam.Resolution.R720p)
gopro.webcamFOV(constants.Webcam.FOV.Linear)
gopro.getWebcamPreview()
gopro.KeepAlive()
