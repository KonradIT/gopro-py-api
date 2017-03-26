from goprocam import GoProCamera
from goprocam import constants
## Test 1: Dump all info
gpCam = GoProCamera.GoPro()
print(gpCam.getStatus(constants.Status.Status,constants.Status.STATUS.Mode))
print(gpCam.getStatusRaw())
print(gpCam.infoCamera(constants.Camera.Name))
print(gpCam.getMedia())
print(gpCam.getMediaInfo("file"))
