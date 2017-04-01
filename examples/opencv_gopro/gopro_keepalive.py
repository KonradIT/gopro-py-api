from goprocam import GoProCamera
from goprocam import constants
gopro = GoProCamera.GoPro()
gopro.stream("udp://127.0.0.1:10000")
