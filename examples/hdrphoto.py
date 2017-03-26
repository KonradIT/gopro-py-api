from goprocam import GoProCamera
from goprocam import constants
gopro = GoProCamera.GoPro(constants.gpcontrol) #HERO4/5 only.

gopro.mode(constants.Mode.PhotoMode, constants.Mode.SubMode.Photo.Single)
gopro.gpControlSet(constants.Photo.PROTUNE_PHOTO, constants.Photo.ProTune.ON)
for i in range(0,9):
	brackets = [constants.Photo.EvComp.P1,
				constants.Photo.EvComp.Zero,
				constants.Photo.EvComp.M1] #Chosen bracketing intervals.
	if str(i) in brackets:
		gopro.gpControlSet(constants.Photo.EVCOMP, str(i))
		name  = ""
		if str(i) == constants.Photo.EvComp.P2:
			name = "Plus_2"
		elif str(i) == constants.Photo.EvComp.P1_5:
			name = "Plus_1.5"
		elif str(i) == constants.Photo.EvComp.P1:
			name = "Plus_1"
		elif str(i) == constants.Photo.EvComp.P0_5:
			name = "Plus_0.5"
		elif str(i) == constants.Photo.EvComp.Zero:
			name = "ZERO_MAIN"
		elif str(i) == constants.Photo.EvComp.M2:
			name = "Minus_2"
		elif str(i) == constants.Photo.EvComp.M1_5:
			name = "Minus_1.5"
		elif str(i) == constants.Photo.EvComp.M1:
			name = "Minus_1"
		elif str(i) == constants.Photo.EvComp.M0_5:
			name = "Minus_0.5"
		gopro.downloadLastMedia(gopro.take_photo(), custom_filename="HDR_"+name+".jpg")
