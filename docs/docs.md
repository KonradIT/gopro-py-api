  
## Docs:

* GoPro(camera='detect', ip_address='10.5.5.9',
mac_address='AA:BB:CC:DD:EE:FF') 
   
### Methods defined here:  

* **IsRecording**(self)
    * Returns either 0 or 1 if the camera is recording or not.

* **KeepAlive**(self)
    * Sends keep alive packet

* **__init__**(self, camera='detect', ip_address='10.5.5.9',
mac_address='AA:BB:CC:DD:EE:FF')
    * Initialize self.  See help(type(self)) for accurate signature.

* **__str__**(self)
    * Return str(self).

* **cancelClip**(self, video_id)
    * cancels clip conversion

* **changeWiFiSettings**(self, ssid, password)
    * Changes ssid and passwod of Hero4 camera

* **clipStatus**(self, status)
    * returns clip status

* **delete**(self, option)
    * Deletes media. "last", "all" or an integer are accepted values for option

* **deleteFile**(self, folder, file)
    * Deletes a file. Pass folder and file as parameters.

* **downloadAll**(self, option='')
    * Download all media on camera

* **downloadLastMedia**(self, path='', custom_filename='')
    * Downloads last media taken, set custom_filename to download to that filename

* **downloadLowRes**(self, path='', custom_filename='')
    * Downloads the low-resolution video

* **downloadMedia**(self, folder, file, custom_filename='')
    * Downloads specific folder and filename

* **downloadMultiShot**(self, path='')
    * Downloads a multi-shot sequence.

* **getClip**(self, file, resolution, frame_rate, start_ms, stop_ms)
    * Starts a clip conversion:  
    * file: folder + filename  
    * resolution: see constants.Clip  
    * frame_rate: see constants.Clip  
    * start_ms: start of the video in ms  
    * stop_ms: stop of the video in ms

* **getClipURL**(self, status)
    * gets clip URL from status

* **getInfoFromURL**(self, url)
    * Gets information from Media URL.

* **getMedia**(self)
    * Returns last media URL

* **getMediaFusion**(self)

* **getMediaInfo**(self, option)
    * Returns an array of the last media, both front and back URLs

* **getPassword**(self)
    * Gets password from Hero3, Hero3+ cameras

* **getPhotoEXIF**(self, option='', folder='', file='')
    * Gets Photo EXIF data, set folder and file parameters.

* **getPhotoInfo**(self, option='', folder='', file='')
    * Gets photo nformation, set folder and file parameters.  
    * option parameters: w/h/wdr/raw...

* **getStatus**(self, param, value='')
    * This returns a status message based on param (status/setting) and value (numeric)

* **getStatusRaw**(self)
    * Delivers raw status message

* **getVideoInfo**(self, option='', folder='', file='')
    * Gets video information, set folder and file parameters.  
option parameters: dur/tag_count/tags/profile/w/h

* **gpControlCommand**(self, param)
    * sends Parameter gpControl/command

* **gpControlExecute**(self, param)
    * sends Parameter to gpControl/execute

* **gpControlSet**(self, param, value)
    * sends Parameter and value to gpControl/setting

* **hilight**(self)
    * Tags a hilight in the video

* **infoCamera**(self, option='')
    * Gets camera info, such as mac address and firmware version. See constants.Camera for possible options.

* **listMedia**(self, format=False, media_array=False)
    * Lists media on SD card  
format = (True/False) - Sets formatting  
media_array = (True/False) - returns an array

* **livestream**(self, option)
    * start livestreaming  
option = "start"/"stop"

* **locate**(self, param)
    * Starts or stops locating (beeps camera)

* **mode**(self, mode, submode='0')
    * Changes mode of the camera. See constants.Mode and constants.Mode.SubMode for sub-modes.

* **overview**(self)

* **pair**(self, usepin=True)
    * This is a pairing procedure needed for HERO4 and HERO5 cameras. When those type GoPro camera are purchased the GoPro Mobile app needs an authentication code when pairing the camera to a mobile device for the first time.   
The code is useless afterwards. This function will pair your GoPro to the
machine without the need of using the mobile app -- at all.

* **parse_value**(self, param, value)

* **power_off**(self)
    * Sends power off command

* **power_on**(self, _mac_address='')
    * Sends power on command. Mac address might need to be defined

* **power_on_auth**(self)
    * Sends power on command to Hero 3/3+ cameras

* **prepare_gpcontrol**(self)

* **reset**(self, r)
    * Resets video/photo/multishot protune values

* **sendBacpac**(self, param, value)
    * sends Parameter and value to 10.5.5.9/camera/

* **sendCamera**(self, param, value='')
    * sends Parameter and value to 10.5.5.9/camera/

* **setZoom**(self, zoomLevel)
    * Sets camera zoom (Hero6/Hero7), zoomLevel is an integer

* **shoot_video**(self, duration=0)
    * Shoots a video, if duration is 0 it will not stop the video, set duration to an integer to set the video duration.

* **shutter**(self, param)
    * Starts/stop video or timelapse recording, pass constants.start or constants.stop as value in param

* **stream**(self, addr, quality='')
    * Starts a FFmpeg instance for streaming to an address  
addr: Address to stream to  
quality: high/medium/low

* **streamSettings**(self, bitrate, resolution)
    * Sets stream settings

* **syncTime**(self)
    * Sets time and date to computer's time and date

* **take_photo**(self, timer=1)
    * Takes a photo. Set timer to an integer to set a wait time

* **video_settings**(self, res, fps='none')
    * Change video resolution and FPS  
See constants.Video.Resolution

* **whichCam**(self)
    * This returns what type of camera is currently connected.  
        - gpcontrol: HERO4 Black and Silver, HERO5 Black and Session, HERO Session (formally known as HERO4 Session), HERO+ LCD, HERO+.  
        - auth: HERO2 with WiFi BacPac, HERO3 Black/Silver/White, HERO3+ Black and Silver.

* * *

Data descriptors defined here:  

* **__dict__**
    * dictionary for instance variables (if defined)

* **__weakref__**
    * list of weak references to the object (if defined)

