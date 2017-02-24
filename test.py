from goprocam import GoProCamera
from goprocam import constants
import time
gpCam = GoProCamera.GoPro()
#gpCam.shutter(constants.start)
gpCam.mode(constants.Mode.VideoMode)
print(gpCam.getStatus(constants.Status.Status,constants.Status.STATUS.Mode))
print(gpCam.getStatusRaw())
print(gpCam.infoCamera(constants.Camera.Name))
print(gpCam.getStatus(constants.Status.Status, constants.Status.STATUS.BatteryLevel))