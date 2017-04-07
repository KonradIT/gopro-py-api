from goprocam import GoProCamera, constants
gpCam = GoProCamera.GoPro()

## Downloads all of the SD card's contents and then formats the sd card.

gpCam.downloadAll()
gpCam.delete("all")