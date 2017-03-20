from goprocam import GoProCamera
from goprocam import constants

gpCam = GoProCamera.GoPro()
while True:
	TIMER=10
	gpCam.downloadLastMedia(gpCam.take_photo(TIMER)) #10 second timelapse. 
