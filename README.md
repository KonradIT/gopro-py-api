# GoPro API for Python 

[![GitHub issues](https://img.shields.io/github/issues/konradit/gopro-py-api.svg)](https://github.com/konradit/gopro-py-api/issues) [![Github All Releases](https://img.shields.io/badge/download-gh-red.svg)](https://github.com/KonradIT/gopro-py-api/releases) [![PyPi Version](http://img.shields.io/pypi/v/goprocam.svg)](https://pypi.python.org/pypi/goprocam)

Unofficial GoPro API Library for Python - connect to GoPro cameras via WiFi.
![](http://i.imgur.com/kA0Rf1b.png)


### Compatibility:

- HERO3
- HERO3+
- HERO4 (including HERO Session)
- HERO+
- HERO5 (including HERO5 Session)
- HERO6 
- Fusion 1

### Installation

From PyPi:

```
pip install goprocam
```

Git (unstable):

```bash
git clone http://github.com/konradit/gopro-py-api
cd gopro-py-api
python setup.py install
```

**Tested on Python 3.6.0** -- **works on Linux and Windows and Mac**

### Documentation:

#### HERO4 and newer (gpcontrol)

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
|     listMedia(option, array) | Outputs a prettified JSON media list, for parsed output option must be True. Optional: ```array``` can be set to True and it will return an array with media items. |
|     getMediaInfo(option) | Gets the media info<br>option=file/folder/size |
|     downloadMedia(folder,file) | Downloads a speficic file, folder and file needed. Example: downloadMedia("104GOPRO","GOPR0001.JPG")
|     downloadLowRes(path) | If video path is specified, it will download the LRV version of the MP4 video (path needs to be a full MP4 video path). If not specified it will get the latest video recorded and download that.<br>Only framerates below 60FPS supported. |
|     getVideoInfo(option, file, folder) | Similar to getMediaInfo() but this will return the video duration or number of hilight tags.<br>Option can be: dur/tag_count/tags/profile. Optional: specify file and folder. |
|     livestream(param) | Starts, restarts or stops the livefeed via UDP. |
|     stream(path) | Streams the gopro feed to a specified ```path```, such as udp://127.0.0.1:10000, FFmpeg needed! |
|     streamSettings(bitrate, resolution) | Sets the live stream's bitrate and resolution (HERO4/5) |
|     pair() | Allows for camera initial pairing, pass usepin=False for HERO5,6 |
|     getClip(file, resolution, fps, start_ms, stop_ms) | Gets a subclip from a video (even a TimeLapse video), similar to GoPro Capture's clip extraction (they do it via http-range) but this one saves it to the SD card.<br>file = the file to get a clip from in the form of [XXX]GOPRO/GOPRXXXX.MP4<br>resolution = the resolution to resize it, constants.Clip.R1080p/R720p/R640p<br>fps = the fps division to perform on the clip: constants.Clip.FPS_NORMAL (leave as is)/FPS_2 (divide by 2)/FPS_4/FPS_8...<br>start_ms & stop_ms = the start and stop time of the clip in milliseconds.

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
|     getVideoInfo(option) | Similar to getMediaInfo() but this will return the video duration or number of hilight tags.<br>Option can be: dur/tag_count/tags/profile. Optional: specify file and folder. |
|     livestream(param) | Starts, restarts or stops the livefeed /live/amba.m3u8 |
|     stream(path) | Streams the gopro feed to a specified ```path```, such as udp://127.0.0.1:10000, FFmpeg needed! |

### Usage:

You can do a ton of stuff with this library, here is a snippet of how some of the commands can be used:

```python
from goprocam import GoProCamera
from goprocam import constants

gpCam = GoProCamera.GoPro()
```

NOTE: You can initialise with ```GoProCamera.GoPro()``` and it will detect which camera is connected and what API to use, this can be unreliable as I have only tested it with HERO4 and HERO3. If you want to connect to a specific camera use ```GoProCamera.GoPro(constants.gpcontrol)``` for HERO4/5/HERO+ and ```GoProCamera.GoPro(constants.auth)``` for HERO3/HERO3+.

If you want to specify a MAC address for the camera (only for HERO4/5/HERO+):

**IMPORTANT**: This is necessary for HERO5 Session/Black and HERO4 Session. 

```GoProCamera.GoPro(mac_address="...")```

---

NOTE: Some commands are HERO4/5 only and viceversa: gpControlCommand/gpControlSet/gpControlExecute are for HERO4/5 only, sendBacpac/sendCamera are HERO3/3+ only. Make sure you use the right constant for getStatus according to your camera.

#### Commands:

* Start or stop

You can start a video or stop it, also take pictures or timelapses. This works with all cameras.

To start a video or take a picture:
```python
gpCam.shutter(constants.start)
```

To stop a video or timelapse:
```python
gpCam.shutter(constants.stop)
```

* Change Modes:

You can change camera modes. Second line only works with HERO4 Black/Silver/Session and HERO5 Black/Session (due to them having Modes and submodes.)

```python
gpCam.mode(constants.Mode.VideoMode)
gpCam.mode(constants.Mode.VideoMode, constants.Video.SubMode.Looping)
```

* Hilight taging:

HERO4 and newer only: You can set a hilight tag on a video.

```python
gpCam.hilight()
```

* Locate camera:

This will make the camera start beeping.

```python
gpCam.locate(constants.start)
...
gpCam.locate(constants.stop)
```

* Turn camera on or off:

Depending on your specified camera, you can turn it on or off with a separate command.

For HERO4 and newer (gpcontrol):

```python
gpCam.power_on()
```

For HERO3/3+ (auth):

```python
gpCam.power_on_auth()
```

To power off, regardless of camera used:

```python
gpCam.power_off()
```

* Quickly take a photo:

You can quickly snap a photo with just one command, you can specify a timer if you wish. This works with all cameras.

```python
gpCam.take_photo(10) #will wait 10 seconds before taking the picture
```

It will return the photo URL

* Quickly shoot a video:

You can start a video with just one command, you can specify the duration of the video, if you don't the video will not be stopped. This works with all cameras.

```python
gpCam.shoot_video() #starts a video
gpCam.shoot_video(40) #shoots a 40 second video
```

* Quickly change the video resolution:

This command will set the video resolution and frame rate specified, it will need to be typed between commas. Make sure your camera supports the video resolution and frame rate specified.

```python
gpCam.video_settings("1080p","30")
gpCam.video_settings("1440p")
```

* Set the correct time:

GoPro cameras need to have the clock set up, otherwise the media metadata will not be correct.

```python
gpCam.syncTime()
```

#### Change settings:

Depending on the camera you have, you will need to change the settings using certain commands.

* HERO4 and newer:

The command ```gpControlSet()``` will allow you to change all the camera's settings. The structure is like follows:

```python
gpCam.gpControlSet(constants.Setup.COMMAND_NAME, constants.Setup.CommandName.Parameter)
```

So, to turn off the beeps on the camera:

```python
gpCam.gpControlSet(constants.Setup.BEEP, constants.Setup.Beep.OFF)
```

The ```constants``` commands are divided into different sections:

	* Video
	* Photo
	* Multishot
	* Setup
	
Each section has its different commands and parameters, so the beep command mentioned above is in setup.

For video, photo, and multishot you can change the resolution, protune values and depeding on the mode you can change mode-specific commands such as TimeLapse interval for Multishot to 10 seconds:

```python
gpCam.gpControlSet(constants.Multishot.TIMELAPSE_INTERVAL, constants.Multishot.TimeLapseInterval.I10)
```

Or the Video+Photo submode interval from video mode to 30 minutes:

```python
gpCam.gpControlSet(constants.Video.VIDEO_PHOTO_INTERVAL, constants.Video.VideoPhotoInterval.Interval30Min)
```

For the complete list of available settings, look in the constants.py file.

* HERO3 / HERO3+

For HERO3/HERO3+ cameras its a bit different, because they use an older version of the API the commands are not the same as HERO4.

```python
gpCam.sendCamera(constants.Hero3Commands.COMMAND_NAME, constants.Hero3Commands.CommandName.Parameter)
```

Most of the settings are on ```constants.Hero3Commands.``` but the ones found in the GoPro Setup section are in ```constants.Hero3Commands.Setup.``` and the settings in Capture Settings are found in ```constants.Hero3Commands.```

* **Hero3Commands**:
	
  * BURST_RATE
  * PHOTO_RESOLUTION
  * CONTINOUOUS_RATE
  * TIMELAPSE_RATE
  * FOV
  * FRAME_RATE
  * VIDEO_RESOLUTION

* **Setup:**

  * BEEP
  * ONE_BTN_MODE
  * ON_SCREEN_DISP
  * DEFAULT_MODE
  * LED
  * NTSC

* **Capture Settings**:

  * VIDEO_PHOTO_INTERVAL
  * LOOPING_VIDEO
  * WHITE_BALANCE
  * ORIENTATION
  * PROTUNE
  * **HERO3+ Black Cameras only:**
	* COLOR_PROFILE
	* SHARPNESS
	* EXPOSURE_COMP
	* SPOT_METER
	* ISO
	
```python
gpCam.sendCamera(constants.Hero3Commands.BURST_RATE, constants.Hero3Commands.BurstRate.BU10_1)
gpCam.sendCamera(constants.Hero3Commands.Setup.LED, constants.Hero3Commands.Setup.StatusLight.OFF)
gpCam.sendCamera(constants.Hero3Commands.CaptureSettings.PROTUNE, constants.Hero3Commands.CaptureSettings.ProTune.ON)
```

#### Status

You can get all status available.

```gpCam.overview()``` will display a simple overview of the camera, such as this one:

For HERO4 and newer:

```
current mode: Video
current submode: Video
current video resolution: 1080p
current video framerate: 30
pictures taken: 78
videos taken:  17
videos left: 01:42:46
pictures left: 3916
battery left: Nearly Empty
space left in sd card: 24.27GB
camera SSID: KonradHERO4Black
Is Recording: Not recording - standby
Clients connected: 1
camera model: HERO4 Black
camera ssid name: KonradHERO4Black
firmware version: HD4.02.05.00.00
```

For HERO3/3+:

```
current mode: Video
current video resolution: 1080p
current photo resolution: 12mp
current timelapse interval: 1s
current video Fov: Wide
status lights: OFF
recording: OFF
```

##### HERO4 and newer:

The status messages are divided into 2 sections, Status and Settings.

In Status, the camera returns the camera in general, for example number of photos taken, battery left, current mode...

In Settings, it returns the status from the id specified, this id is a command from the constants file that works in gpControlSet()

You can use getStatus() to query the status messages.

```python
gpCam.getStatus(constants.Status.Status,constants.Status.STATUS.Mode) #Gets current mode status
0

gpCam.getStatus(constants.Status.Status, constants.Status.STATUS.BatteryLevel) #Gets battery level
3

gpCam.getStatus(constants.Status.Settings, constants.Setup.ORIENTATION) #Gets orientation mode
2

```

This returns the raw value, to convert it into something we can easily recognise you use parse_value()

```python
gpCam.parse_value("video_left",gpCam.getStatus(constants.Status.Status, constants.Status.STATUS.RemVideoTime))
'01:42:50'

gpCam.parse_value("video_res",gpCam.getStatus(constants.Status.Settings, constants.Video.RESOLUTION))
'1080p'

gpCam.parse_value("battery", gpCam.getStatus(constants.Status.Status, constants.Status.STATUS.BatteryLevel))
'Full'
```

To get information about the camera, such as the name or firmware version with infoCamera():

```python
print(gpCam.infoCamera(constants.Camera.Name)) #Gets camera name
HERO4 Black
print(gpCam.infoCamera(constants.Camera.Firmware)) #Gets camera fw version
HD4.02.05.00.00
```

##### HERO3 / HERO3+:

Very similar to ```sendCamera()```, you can input any value you want to get and it will return it.

The status messages are in ```constants.Hero3Status.```. This will return the raw value.

```python
gpCam.getStatus(constants.Hero3Status.WhiteBalance)
'00'
gpCam.getStatus(constants.Hero3Status.IsRecording)
'01'
gpCam.getStatus(constants.Hero3Status.PicRes)
'5'
```

To translate those values to something we can understand:

```python
gpCam.parse_value(constants.Hero3Status.PicRes, gpCam.getStatus(constants.Hero3Status.PicRes))
'12mp'
gpCam.parse_value(constants.Hero3Status.TimeLapseInterval, gpCam.getStatus(constants.Hero3Status.TimeLapseInterval))
'1s'
gpCam.parse_value(constants.Hero3Status.Mode, gpCam.getStatus(constants.Hero3Status.Mode))
'Video'
```

#### Media

This is camera agnostic:
	
* Get the url of latest video or picture taken

```python
print(gpCam.getMedia()) #Latest media taken URL
http://10.5.5.9:8080/videos/DCIM/104GOPRO/GOPR2386.JPG
```

* Get the latest media's filename/size:

```
print(gpCam.getMediaInfo("file")) #Latest media taken filename
GOPR2386.JPG
print(gpCam.getMediaInfo("size")) #Latest media taken size
14.82MB
```

* Download the latest media:

```python
gpCam.downloadLastMedia() #Downloads last video/photo taken
```

* Download a certain URL (or snap something and download it.):

```python
gpCam.downloadLastMedia(gpCam.take_photo(5)) #Waits 5 seconds, takes a photo, downloads it to current directory.
gpCam.downloadLastMedia(gpCam.shoot_video(120)) #Shoots a 120 second video and then downloads it.
```

* Download a video in low resolution:

You can download a video that is recorded in 1080p or below in low resolution. This enables fast transfer of videos but the low res videos are only intended to be used as a reference for the actual high quality video.

```python
gpCam.downloadLowRes() #video is already recorded, now this downloads the low resolution version
gpCam.downloadLowRes(gpCam.shoot_video(120)) #Record a 120 second video and download it in low resolution
```

* Download all media on the camera:

```python
gpCam.downloadAll() #downloads all media
gpCam.downloadAll("photos") #downloads only all photos
gpCam.downloadAll("videos") #downloads all videos
```

* Download a specific media:

```python
gpCam.downloadMedia("100GOPRO","GOPR0045.MP4")
```

* Get video metadata:

```python
gpCam.getVideoInfo("dur", "GOPR2524.MP4") #gets video duration
24

gpCam.getVideoInfo("tags", "GOPR2524.MP4") #get an array of hilight tags in ms
[5872, 7907] 

gpCam.getVideoInfo("tag_count", "GOPR2524.MP4")
2
```

* Delete:

All:

```python
gpCam.delete("all")
```

Last:

```python
gpCam.delete("last")
```

A specific file:

```python
gpCam.deleteFile("104GOPRO","GOPR0038.JPG")
```

* List camera media contents:

```python
gpCam.listMedia()
```

it will return a JSON list of the media files available on the camera:

```
{
  "id": "3993129928403681535",
  "media": [
    {
      "d": "104GOPRO",
      "fs": [
        {
          "mod": "1490468532",
          "n": "GOPR2760.JPG",
          "s": "4919786"
        },
        {
          "mod": "1490468536",
          "n": "GOPR2761.JPG",
          "s": "4942872"
        },
        {
          "mod": "1490468540",
          "n": "GOPR2762.JPG",
          "s": "4943428"
        },

```

If you want it formatted:

```python
gpCam.listMedia(format=True)
```

```
folder: 104GOPRO
GOPR2760.JPG
GOPR2761.JPG
GOPR2762.JPG
GOPR2763.JPG
GOPR2764.MP4
GOPR2765.MP4
GOPR2766.MP4
GOPR2767.MP4
GOPR2768.MP4
```

will return it in a new line each.

Lastly, if you want it in an array:

```python
gpCam.listMedia(format=True, media_array=True)
```

```
[['100GOPRO', 'GOPR3132.MP4', '741578340'], ['100GOPRO', 'GOPR3133.MP4', '61818786'], ['100GOPRO', 'GOPR3134.MP4', '52298492'], ['100GOPRO', 'GOPR3135.MP4', '22484879']]
```

```
>>> m=gopro.listMedia(True, True)
>>> m[0] #First media item
['100GOPRO', 'GOPR3132.MP4', '741578340']
>>> m[1] Second media item
['100GOPRO', 'GOPR3133.MP4', '61818786']
>>> m[2] Third media item
['100GOPRO', 'GOPR3134.MP4', '52298492']
>>> m[2][1] #Get name of third media item
'GOPR3134.MP4'
>>> m[2][0] #Get folder of third media item
'100GOPRO'
>>> m[2][2] #Get size (bytes) of first media item
'52298492'

```

### Pairing:

If you don't want to use the GoPro APP to pair your camera for the first time you can pair it with this API.

```
...
gopro = GoProCamera.GoPro()
gopro.pair(usepin=False) # GoPro HERO 5, HERO 6

```

### Streaming:

In regards to streaming, this library provides with the following functions:

This will enable livestreaming on all cameras.

```python
gpCam.livestream("start")
gpCam.livestream("stop")
```

To stream GoPro feed to another place such as localhost (this is needed for HERO4/5):

```python
gpCam.stream("udp://localhost:5000")
```

You can also set the quality of the stream, HERO5 supports 720p!

```python
gpCam.streamSettings(constants.Stream.Bitrate.B4Mbps, constants.Stream.WindowSize.R480) #For HERO4

gpCam.streamSettings(constants.Stream.Bitrate.B4Mbps, constants.Stream.WindowSize.R720) #For HERO5
```

For HERO3 do the same steps above.

See the [examples/opencv_gopro](examples/opencv_gopro) folder for a python script to open the HERO4/5 feed in openCV and detect faces. On [examples/streaming](examples/streaming) there are scripts to stream the GoPro live feed to Facebook, YouTube or Twitch.

### Video screencap:

* HERO4 Black: https://vimeo.com/209079783
* HERO4 Session: https://vimeo.com/209129019
* HERO3 Black: https://vimeo.com/209181246
* HERO5 Black: https://vimeo.com/235135652
