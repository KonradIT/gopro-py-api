from goprocam import GoProCamera
from goprocam import constants

gpCam = GoProCamera.GoPro(constants.auth)
print(gpCam.getStatusRaw())
gpCam.infoCamera("model_name")
gpCam.getStatus(constants.Hero3Status.Mode)
gpCam.getStatus(constants.Hero3Status.SpotMeter)
gpCam.getStatus(constants.Hero3Status.TimeLapseInterval)
gpCam.getStatus(constants.Hero3Status.FOV)
gpCam.getStatus(constants.Hero3Status.Beep)
gpCam.getStatus(constants.Hero3Status.AutoOff)
gpCam.getStatus(constants.Hero3Status.VideoRes)
gpCam.getStatus(constants.Hero3Status.FPS)
gpCam.getStatus(constants.Hero3Status.Loop)
gpCam.getStatus(constants.Hero3Status.IsRecording)
