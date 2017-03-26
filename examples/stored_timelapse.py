from goprocam import GoProCamera
from goprocam import constants
gopro = GoProCamera.GoPro()
TIMER=5
COUNT=0
while True:
	COUNT += 1
	gopro.downloadLastMedia(gopro.take_photo(TIMER), "TL" + str(COUNT) + ".jpg")
	gopro.delete("last")
