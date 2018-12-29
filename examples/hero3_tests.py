from goprocam import GoProCamera
from goprocam import constants

gpCam = GoProCamera.GoPro(constants.auth)

gpCam.infoCamera("model_name")
print(gpCam.getStatus(constants.Hero3Status.SpotMeter))
print(gpCam.getStatus(constants.Hero3Status.TimeLapseInterval))
print(gpCam.getStatus(constants.Hero3Status.FOV))
print(gpCam.getStatus(constants.Hero3Status.Beep))
print(gpCam.getStatus(constants.Hero3Status.LED))
print(gpCam.getStatus(constants.Hero3Status.AutoOff))
print(gpCam.getStatus(constants.Hero3Status.VideoRes))
print(gpCam.getStatus(constants.Hero3Status.FPS))
print(gpCam.getStatus(constants.Hero3Status.Loop))
print(gpCam.getStatus(constants.Hero3Status.WhiteBalance))
print(gpCam.getStatus(constants.Hero3Status.IsRecording))
print(gpCam.getStatus(constants.Hero3Status.PicRes))
print(gpCam.getStatus(constants.Hero3Status.TimeRecordedMins))
print(gpCam.getStatus(constants.Hero3Status.TimeRecordedSecs))
print(gpCam.getStatus(constants.Hero3Status.Charging))
print(gpCam.getStatus(constants.Hero3Status.PicturesTaken))
print(gpCam.getStatus(constants.Hero3Status.VideoRemaining))
print(gpCam.getStatus(constants.Hero3Status.VideosTaken))
