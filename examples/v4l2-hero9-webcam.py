import sys
from goprocam import GoProCamera, constants
gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP(sys.argv[1]), camera=constants.gpcontrol, webcam_device=sys.argv[1])
gopro.webcamFOV(constants.Webcam.FOV.Wide)
gopro.startWebcam()

