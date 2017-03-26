from goprocam import GoProCamera
from goprocam import constants
import time
gpCam = GoProCamera.GoPro()
print(gpCam.take_photo(10))

