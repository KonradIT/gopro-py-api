from goprocam import GoProCamera
from goprocam import constants

gpCam = GoProCamera.GoPro()
TIMER=10
gpCam.downloadLastMedia(gpCam.take_photo(TIMER)) #take a photo in 4 seconds and download it.
