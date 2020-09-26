from signal import signal, SIGINT
from goprocam import GoProCamera, constants

def handler(s, f):
    gopro.stopWebcam()
    quit()

signal(SIGINT, handler)

gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP())
gopro.startWebcam(constants.Webcam.Resolution.R720p)
gopro.webcamFOV(constants.Webcam.FOV.Linear)
gopro.getWebcamPreview()
gopro.KeepAlive()
