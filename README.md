# GoPro API for Python 

Unofficial GoPro API Library for Python - connect to HERO3/3+/4/5/+ via WiFi.

![](http://i.imgur.com/kA0Rf1b.png)


###Compatibility:

- HERO3
- HERO3+
- HERO4 (including HERO Session)
- HERO+
- HERO5

###Installation

```bash
pip install goproapi
```

Or from source

```bash
git clone http://github.com/konradit/gopropy
cd gopropy
python setup.py install
```

###Usage:

You can do a ton of stuff with this library, here is a snippet of how some of the commands can be used:

```python
from goprocam import GoProCamera
from goprocam import constants

gpCam = GoProCamera.GoPro()

gpCam.shutter(constants.start) #starts shooting or takes a photo

gpCam.mode(constants.Mode.VideoMode) #changes to video mode

print(gpCam.getStatus(constants.Status.Status,constants.Status.STATUS.Mode)) #Gets current mode status
>0
print(gpCam.infoCamera(constants.Camera.Name)) #Gets camera name
>HERO4 Black
print(gpCam.getStatus(constants.Status.Status, constants.Status.STATUS.BatteryLevel)) #Gets battery level
>3
print(gpCam.getMedia()) #Latest media taken URL
>http://10.5.5.9:8080/videos/DCIM/104GOPRO/GOPR2386.JPG
print(gpCam.getMediaInfo("file")) #Latest media taken filename
>GOPR2386.JPG
```

