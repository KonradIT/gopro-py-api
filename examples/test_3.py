from goprocam import GoProCamera
from goprocam import constants
import time
gpCam = GoProCamera.GoPro(constants.auth)
gpCam.overview()
gpCam.listMedia(True)
