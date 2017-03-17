from goprocam import GoProCamera
from goprocam import constants
import time
gpCam = GoProCamera.GoPro()
#gpCam.shutter(constants.start)

print(gpCam.take_photo(10))
#gpCam.power_off()
