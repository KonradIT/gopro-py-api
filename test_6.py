from goprocam import GoProCamera
from goprocam import constants

gpCam = GoProCamera.GoPro(constants.auth)
print(gpCam.getStatusRaw())
gpCam.infoCamera("model_name")
gpCam.debug(constants.Hero3Status.Mode)
gpCam.debug(constants.Hero3Status.SpotMeter)
gpCam.debug(constants.Hero3Status.TimeLapseInterval)
gpCam.debug(constants.Hero3Status.FOV)
gpCam.debug(constants.Hero3Status.Beep)
gpCam.debug(constants.Hero3Status.AutoOff)
gpCam.debug(constants.Hero3Status.VideoRes)
gpCam.debug(constants.Hero3Status.FPS)
gpCam.debug(constants.Hero3Status.Loop)
gpCam.debug(constants.Hero3Status.IsRecording)
