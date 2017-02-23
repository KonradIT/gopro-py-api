from goprocam import GoProCamera
from goprocam import constants
gpCam = GoProCamera.GoPro()
#gpCam.shutter(constants.start)
print(gpCam.getStatus("status","8"))