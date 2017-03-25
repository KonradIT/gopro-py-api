# GoPro API for Python 

[![GitHub issues](https://img.shields.io/github/issues/konradit/gopro-py-api.svg)](https://github.com/konradit/gopro-py-api/issues) [![Github All Releases](https://img.shields.io/github/downloads/konradit/gopro-py-api/total.svg)]() [![PyPI](https://img.shields.io/pypi/v/goprocam.svg)]() [![PyPI](https://img.shields.io/pypi/dm/goprocam.svg)]()

Unofficial GoPro API Library for Python - connect to HERO3/3+/4/5/+ via WiFi.

![](http://i.imgur.com/kA0Rf1b.png)


### Compatibility:

- HERO3
- HERO3+
- HERO4 (including HERO Session)
- HERO+
- HERO5

### Installation

From PyPi:

```
pip install goprocam
```

Git (unstable):

```bash
git clone http://github.com/konradit/gopro_py_api
cd gopro-py-api
python setup.py install
```

**Tested on Python 3.6.0** -- **works on Linux and Windows**

### Documentation:

#### HERO4/HERO5/HERO+ (gpcontrol)

These cameras use a new version of GoPro API which centers around /gp/gpControl/ url.

| Code | Explanation |
|------|-------------|
|     gpControlCommand(X,Y) | Sends a command to the camera, using GoPro constants |
|     gpControlSet(X,Y) | Sends a setting to the camera, using GoPro constants |
|     shutter(param) | Starts a video or takes a picture<br>param=constants.start or constants.stop |
|     shoot_video(X) | Shoots a video, X is the number of seconds the video will be, default 0, (infinity) |
|     take_photo(X) | Takes a photo, X is the time before the picture is taken. Default 0. Returns URL |
|     video_settings(X,Y) | Changes the video settings<br><ul><li>X=Video Resolution: 4k / 2k / 1440p / 1080p / 960p / 480p</li><li>Y=Frame Rate: 240 / 120 / 100 / 60 / 30 / 24 </li></ul>|
|     mode(X,Y) | Changes the mode, X=Mode, Y=Submode (default is 0). Example: camera_mode(constants.Mode.PhotoMode, constants.Mode.SubMode.Photo.Single) |
|     getStatusRaw() | Returns the status dump of the camera in json |
|     getStatus(X,Y) | Returns the status. <br><ul><li>X = constants.Status.Status or constants.Status.Settings</li><li>Y = status id (Status/Setup/Video/Photo/MultiShot).</li><li>NOTE: This returns the status of the camera as an integer.</li></ul>|
|     infoCamera(option) | Returns camera information<br>option = constants.Camera.Name/Number/Firmware/SerialNumber/SSID/MacAddress |
|     overview() | Prints a general overview of the camera status. | 
|     parse_value(X,Y) | Parses integers to human strings (mode/sub_mode/rem_space/etc...) |
|     delete() | Can be: delete(last) or delete(all) |
|     deleteFile(folder,file) | Deletes a specific file |
|     hilight() | HiLights a moment in the video recording |
|     power_on() | Powers the camera on. NOTE: run this to put your H4 Session into app mode first! |
|     power_off() | Powers the camera off |
|     syncTime() | Syncs the camera time to the computer's time |
|     locate(param) | Makes the camera beep. locate(constants.Locate.Start) for start and locate(constants.Locate.Stop) for stop. |
|     getMedia() | returns the last media taken URL |
|     downloadLastMedia() | Downloads latest media taken |
|     downloadMedia(folder, file) | Downloads specified file, eg: 100GOPRO, GOPR0005.MP4 |
|     listMedia(option) | Outputs a prettified JSON media list, for parsed output option must be True |
|     getMediaInfo(option) | Gets the media info<br>option=file/folder/size |
|     downloadMedia(folder,file) | Downloads a speficic file, folder and file needed. Example: downloadMedia("104GOPRO","GOPR0001.JPG")
|     downloadLowRes(path) | If video path is specified, it will download the LRV version of the MP4 video (path needs to be a full MP4 video path). If not specified it will get the latest video recorded and download that.<br>Only framerates below 60FPS supported. |
|     getVideoInfo(option) | Similar to getMediaInfo() but this will return the video duration or number of hilight tags.<br>Option can be: dur/tag_count/tags/profile |
|     livestream(param) | Starts, restarts or stops the livefeed via UDP. |

#### HERO3/HERO3+/HERO2 (auth):

These cameras use the traditional /camera/ or /bacpac/ GoPro API, which is now deprecated and replaced with gpControl for newer cameras starting with HERO 4.

| Code | Explanation |
|------|-------------|
|     sendCamera(X,Y) | Sends a command to the camera using /camera/. Use constants.Hero3Commands. |
|     sendBacpac(X,Y) | Sends a command to the camera using /bacpac/. Use constants.Hero3Commands. |
|     shutter(param) | Starts a video or takes a picture<br>param=constants.start or constants.stop |
|     shoot_video(X) | Shoots a video, X is the number of seconds the video will be, default 0, (infinity) |
|     take_photo(X) | Takes a photo, X is the time before the picture is taken. Default 0. |
|     video_settings(X,Y) | Changes the video settings<br><ul><li>X=Video Resolution: 4k / 2k / 1440p / 1080p / 960p / 480p</li><li>Y=Frame Rate: 240 / 120 / 100 / 60 / 30 / 24 </li></ul>|
|     mode(X,Y) | Changes the mode, X=Mode: constants.Hero3Commands.Mode.VideoMode/PhotoMode/BurstMode/TimeLapseMode |
|     getStatusRaw() | Returns the status dump of the camera in json |
|     getStatus(status) | Gets camera status, status can be constants.Hero3Status.Mode/SpotMeter/TimeLapseInterval/FOV/Beep/LED/AutoOff/VideoRes/FPS/Loop/WhiteBalance/IsRecording/Pictures |
|     infoCamera(option) | Returns camera information<br>option = model_name, firmware_version, ssid
|     delete() | Can be: delete(last) or delete(all) |
|     deleteFile(folder,file) | Deletes a specific file |
|     power_on_auth() | Powers the camera on. |
|     power_off() | Powers the camera off |
|     syncTime() | Syncs the camera time to the computer's time |
|     getMedia() | returns the last media taken URL |
|     downloadLastMedia() | Downloads latest media taken |
|     listMedia() | Outputs a prettified JSON media list |
|     getMediaInfo(option) | Gets the media info<br>option=file/folder/size |
|     downloadMedia(folder,file) | Downloads a speficic file, folder and file needed. Example: downloadMedia("104GOPRO","GOPR0001.JPG")
|     downloadLowRes(path) | If video path is specified, it will download the LRV version of the MP4 video (path needs to be a full MP4 video path). If not specified it will get the latest video recorded and download that.<br>Only framerates below 60FPS supported. |
|     getVideoInfo(option) | Similar to getMediaInfo() but this will return the video duration or number of hilight tags.<br>Option can be: dur/tag_count/tags/profile |
|     livestream(param) | Starts, restarts or stops the livefeed /live/amba.m3u8 |

### Usage:

You can do a ton of stuff with this library, here is a snippet of how some of the commands can be used:

```python
from goprocam import GoProCamera
from goprocam import constants

gpCam = GoProCamera.GoPro()
```

NOTE: You can initialise with ```GoProCamera.GoPro()``` and it will detect which camera is connected and what API to use, this can be unreliable as I have only tested it with HERO4 and HERO3. If you want to connect to a specific camera use ```GoProCamera.GoPro(constants.gpcontrol)``` for HERO4/5/HERO+ and ```GoProCamera.GoPro(constants.auth)``` for HERO3/HERO3+.

---

NOTE: Some commands are HERO4/5 only and viceversa: gpControlCommand/gpControlSet/gpControlExecute are for HERO4/5 only, sendBacpac/sendCamera are HERO3/3+ only. Make sure you use the right constant for getStatus according to your camera.

```python
gpCam.shutter(constants.start) #starts shooting or takes a photo

gpCam.mode(constants.Mode.VideoMode) #changes to video mode

print(gpCam.getStatus(constants.Status.Status,constants.Status.STATUS.Mode)) #Gets current mode status
>0

print(gpCam.infoCamera(constants.Camera.Name)) #Gets camera name
>HERO4 Black

print(gpCam.getStatus(constants.Status.Status, constants.Status.STATUS.BatteryLevel)) #Gets battery level
>3

print(gpCam.getStatus(constants.Status.Settings, constants.Setup.ORIENTATION)) #Gets orientation mode
>2

print(gpCam.getMedia()) #Latest media taken URL
>http://10.5.5.9:8080/videos/DCIM/104GOPRO/GOPR2386.JPG

print(gpCam.getMediaInfo("file")) #Latest media taken filename
>GOPR2386.JPG

gpCam.take_photo(5) #Takes a photo in 5 seconds.

gpCam.shoot_video(60) #Shoots a 60 second video

gpCam.video_settings("1080p","60") #Changes resolution to 1080p60

gpCam.gpControlSet(constants.Setup.BEEP, constants.Setup.Beep.OFF) #Disable beeps.

gpCam.gpControlSet(constants.Video.SPOT_METER, constants.Video.SpotMeter.ON) #Activates spot meter on video mode

gpCam.overview()
>camera overview
>current mode: Video
>current submode: Video
>current video resolution: 1080p
>current video framerate: 30
>pictures taken: 27
>videos taken:  15
>videos left: 01:21:19
>pictures left: 3099
>battery left: Halfway
>space left in sd (GBs): 20.62
>camera SSID: KonradHERO4Black
>Is Recording: Not recording - standby
>Clients connected: 1
>camera model: HERO4 Black
>camera ssid name: KonradHERO4Black
>firmware version: HD4.02.05.00.00
>serial number: CXXXXXXXXXXXXX

gpCam.downloadLastMedia() #Downloads last video/photo taken

gpCam.downloadLastMedia(gpCam.take_photo(5)) #Waits 5 seconds, takes a photo, downloads it to current directory.

gpCam.getVideoInfo("dur", "GOPR2524.MP4") #gets video duration
>24

```

### Video screencap:

* HERO4 Black: https://vimeo.com/209079783
* HERO4 Session: https://vimeo.com/209129019
* HERO3 Black: https://vimeo.com/209181246
* HERO5 Black: 