from goprocam import GoProCamera, constants
gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP())
gopro.startWebcam(constants.Webcam.Resolution.R720p)
gopro.webcamFOV(constants.Webcam.FOV.Linear)
gopro.getWebcamPreview()
