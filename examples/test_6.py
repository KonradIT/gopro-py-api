from goprocam import GoProCamera
from goprocam import constants

gpCam = GoProCamera.GoPro(constants.auth)

gpCam.infoCamera("model_name")

if gpCam.getStatus(constants.Hero3Status.Mode) == 00:
	print("videomode")
gpCam.getStatus(constants.Hero3Status.SpotMeter)
gpCam.getStatus(constants.Hero3Status.TimeLapseInterval)
gpCam.getStatus(constants.Hero3Status.FOV)
gpCam.getStatus(constants.Hero3Status.Beep)
gpCam.getStatus(constants.Hero3Status.LED)
gpCam.getStatus(constants.Hero3Status.AutoOff)
gpCam.getStatus(constants.Hero3Status.VideoRes)
gpCam.getStatus(constants.Hero3Status.FPS)
gpCam.getStatus(constants.Hero3Status.Loop)
gpCam.getStatus(constants.Hero3Status.WhiteBalance)
gpCam.getStatus(constants.Hero3Status.IsRecording)
gpCam.getStatus(constants.Hero3Status.PicRes)
gpCam.getStatus(constants.Hero3Status.TimeRecordedMins)
gpCam.getStatus(constants.Hero3Status.TimeRecordedSecs)
gpCam.getStatus(constants.Hero3Status.Charging)
gpCam.getStatus(constants.Hero3Status.PicturesTaken)

gpCam.getStatus(constants.Hero3Status.VideoRemaining)
gpCam.getStatus(constants.Hero3Status.VideosTaken)
