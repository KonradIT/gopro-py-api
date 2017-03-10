import time
import socket
import urllib.request
import json
import re
from goprocam import constants
import datetime
import struct
import subprocess
from socket import timeout
from urllib.error import HTTPError
from urllib.error import URLError

##################################################
# Preface:                                       #
# This API Library works with All GoPro cameras, #
# it detects which camera is connected and sends #
# the appropiate URL with values.                #
##################################################

class GoPro:
	def prepare_gpcontrol(self):
		time.sleep(2)
		try:
			response_raw = urllib.request.urlopen('http://10.5.5.9/gp/gpControl', timeout=5).read()
			jsondata=json.loads(response_raw)
			response=jsondata["info"]["firmware_version"]
			if "HD4" in response or "HD3.2" in response or "HD5" in response or "HX" in response:
				while self.getStatus(constants.Status.Status, constants.Status.STATUS.IsConnected) == 0:
					self.getStatus(constants.Status.Status, constants.Status.STATUS.IsConnected)
		except (HTTPError, URLError) as error:
			self.prepare_gpcontrol()
		except timeout:
			self.prepare_gpcontrol()
		
		print("Camera successfully connected!")
	def __init__(self, camera="detect", mac_address="AA:BB:CC:DD:EE:FF"):
		self.ip_addr = "10.5.5.9"
		self._camera=""
		self._mac_address=mac_address
		if camera == "detect":

			try:
				response_raw = urllib.request.urlopen('http://10.5.5.9/gp/gpControl', timeout=5).read()
				jsondata=json.loads(response_raw)
				response=jsondata["info"]["firmware_version"]
				if "HD4" in response or "HD3.2" in response or "HD5" in response or "HX" in response:
					self.prepare_gpcontrol()
					self._camera="gpcontrol"
				else:
					response = urllib.request.urlopen('http://10.5.5.9/camera/cv',timeout=5).read()
					if b"Hero3" in response:
						self._camera="auth"
			except (HTTPError, URLError) as error:
				try:
					response = urllib.request.urlopen('http://10.5.5.9/camera/cv',timeout=5).read()
					if b"Hero3" in response:
						self._camera="auth"
					else:
						self.prepare_gpcontrol()
				except (HTTPError, URLError) as error:
					self.power_on(self._mac_address)
					time.sleep(5)
				except timeout:
					self.power_on(self._mac_address)
					time.sleep(5)
			except timeout:
				self.power_on(self.mac_address)
				time.sleep(5)
				response = urllib.request.urlopen('http://10.5.5.9/camera/cv',timeout=5).read()
				if b"Hero3" in response:
					self._camera="auth"
				else:
					self.prepare_gpcontrol()
			
		else:
			if camera == "auth" or camera == "HERO3" or camera == "HERO3+" or camera == "HERO2":
				self._camera="auth"
			elif camera == "gpcontrol" or camera == "HERO4" or camera == "HERO5" or camera == "HERO+":
				self._camera="gpcontrol"
				self.power_on(self._mac_address)
				self.prepare_gpcontrol()
			print("Connected to " + self.ip_addr)
	
	def getPassword(self):
		try:
			PASSWORD = urllib.request.urlopen('http://10.5.5.9/bacpac/sd', timeout=5).read()
			password = str(PASSWORD, 'utf-8')
			password_parsed=re.sub(r'\W+', '', password)
			return password_parsed
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def gpControlSet(self, param,value):
		#sends Parameter and value to gpControl/setting
		try:
			return urllib.request.urlopen('http://10.5.5.9/gp/gpControl/setting/' + param + '/' + value, timeout=5).read().decode('utf-8')
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	
	def gpControlCommand(self, param):
		try:
			return urllib.request.urlopen('http://10.5.5.9/gp/gpControl/command/' + param, timeout=5).read().decode('utf-8')
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def gpControlExecute(self, param):
		try:
			return urllib.request.urlopen('http://10.5.5.9/gp/gpControl/execute?' + param, timeout=5).read().decode('utf-8')
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def sendCamera(self, param,value=None):
		value_notemtpy = ""
		if value:
			value_notempty=str('&p=%' + value)
		#sends parameter and value to /camera/
		try:
			urllib.request.urlopen('http://10.5.5.9/camera/' + param + '?t=' + self.getPassword() + value_notempty, timeout=5).read()
		except (HTTPError, URLError) as error:
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")	
	
	
	def sendBacpac(self, param,value):
		#sends parameter and value to /bacpac/
		value_notemtpy = ""
		if value:
			value_notempty=str('&p=%' + value)
		try:
			urllib.request.urlopen('http://10.5.5.9/bacpac/' + param + '?t=' + self.getPassword() + value_notempty, timeout=5).read()
		except (HTTPError, URLError) as error:
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		
	
	
	def whichCam(self):
		# This returns what type of camera is currently connected.
		# gpcontrol: HERO4 Black and Silver, HERO5 Black and Session, HERO Session (formally known as HERO4 Session), HERO+ LCD, HERO+.
		# auth: HERO2 with WiFi BacPac, HERO3 Black/Silver/White, HERO3+ Black and Silver.
		if self._camera != "":
			return self._camera
		else:
			self.power_on(self._mac_address)
			time.sleep(5)
			try:
				response_raw = urllib.request.urlopen('http://10.5.5.9/gp/gpControl', timeout=5).read()
				jsondata=json.loads(response_raw)
				response=jsondata["info"]["firmware_version"]
				if "HD4" in response or "HD3.2" in response or "HD5" in response or "HX" in response:
					self.prepare_gpcontrol()
					self._camera="gpcontrol"
				else:
					response = urllib.request.urlopen('http://10.5.5.9/camera/cv',timeout=5).read()
					if b"Hero3" in response:
						self._camera="auth"
			except (HTTPError, URLError) as error:
				response = urllib.request.urlopen('http://10.5.5.9/camera/cv',timeout=5).read()
				if b"Hero3" in response:
					self._camera="auth"
				else:
					self.prepare_gpcontrol()
			except timeout:
				response = urllib.request.urlopen('http://10.5.5.9/camera/cv',timeout=5).read()
				if b"Hero3" in response:
					self._camera="auth"
				else:
					self.prepare_gpcontrol()
			return self._camera
	
	
	def getStatus(self, param, value):
		try:
			req=urllib.request.urlopen("http://10.5.5.9/gp/gpControl/status", timeout=5)
			data = req.read()
			encoding = req.info().get_content_charset('utf-8')
			json_data = json.loads(data.decode(encoding))
			return json_data[param][value]
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	
	
	def getStatusRaw(self):
		if self.whichCam() == "gpcontrol":
			try:
				return urllib.request.urlopen("http://10.5.5.9/gp/gpControl/status", timeout=5).read().decode('utf-8')
			except (HTTPError, URLError) as error:
				return ""
				print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
			except timeout:
				return ""
				print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		elif self.whichCam() == "auth":
			try:
				return urllib.request.urlopen("http://10.5.5.9/bacpac/se?t=" + self.getPassword(), timeout=5).read()
			except (HTTPError, URLError) as error:
				return ""
				print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
			except timeout:
				return ""
				print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		else:
			print("Error, camera not defined.")
	
	def infoCamera(self, option):
		if self.whichCam() == "gpcontrol":
			try:
				info=urllib.request.urlopen('http://10.5.5.9/gp/gpControl', timeout=5)
				data = info.read()
				encoding = info.info().get_content_charset('utf-8')
				parse_read = json.loads(data.decode(encoding))
				return parse_read["info"][option]
			except (HTTPError, URLError) as error:
				return ""
				print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
			except timeout:
				return ""
				print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		elif self.whichCam() == "auth":
			if option == "model_name" or option == "firmware_version":
				try:
					info=urllib.request.urlopen('http://10.5.5.9/camera/cv', timeout=5)
					data = info.read()
					parsed=re.sub(r'\W+', '', str(data))
					print(parsed)
				except (HTTPError, URLError) as error:
					return ""
					print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
				except timeout:
					return ""
					print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
			if option == "ssid":
				try:
					info=urllib.request.urlopen('http://10.5.5.9/bacpac/cv', timeout=5)
					data = info.read()
					parsed=re.sub(r'\W+', '', str(data))
					print(parsed)
				except (HTTPError, URLError) as error:
					return ""
					print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
				except timeout:
					return ""
					print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		else:
			print("Error, camera not defined.")
	
	def shutter(self,param):
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("shutter?p=" + param))
		else:
			if len(param) == 1:
				param = "0" + param
			self.sendBacpac("SH",param)
	
	
	def mode(self, mode, submode="0"):
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("sub_mode?mode=" + mode + "&sub_mode=" + submode))
		else:
			if len(mode) == 1:
				mode = "0" + mode
			self.sendBacpac("CM",mode)
	def delete(self, option):
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("storage/delete/" + option))
		else:
			if option == "last":
				print(self.sendCamera("DL"))
			if option == "all":
				print(self.sendCamera("DA"))
	def deleteFile(self, folder,file):
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("storage/delete?p=" + folder + "/" + file))
		else:
			print(self.sendCamera("DA",folder+"/"+file))
	def locate(self, param):
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("system/locate?p=" + param))
		else:
			print(self.sendCamera("LL","0"+param))
				
	def hilight(self):
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("storage/tag_moment"))
		else:
			print("Not supported.")
	
	def power_off(self):
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("system/sleep"))
		else:
			print(self.sendBacpac("PW","00"))
			
	def power_on(self,mac_address="AA:BB:CC:DD:EE:FF"):
		#Wake On Lan:
		print("Waking up...")
		
		if mac_address is None:
				mac_address = "AA:BB:CC:DD:EE:FF"
		else:
				mac_address = str(mac_address)
				if len(mac_address) == 12:
						pass
				elif len(mac_address) == 17:
						sep = mac_address[2]
						mac_address = mac_address.replace(sep, '')
				else:
						raise ValueError('Incorrect MAC address format')

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		data = bytes('FFFFFFFFFFFF' + mac_address * 16, 'utf-8')
		message = b''
		for i in range(0, len(data), 2):
				message += struct.pack(b'B', int(data[i: i + 2], 16))
		sock.sendto(message, ("10.5.5.9", 9))
		
	def power_on_auth():
		print(self.sendBacpac("PW","01"))
	def video_settings(self, res, fps="none"):
		if self.whichCam() == "gpcontrol":
			x="constants.Video.Resolution.R" + res
			videoRes = eval(x)
			print(self.gpControlSet(constants.Video.RESOLUTION,videoRes))
			if fps != "none":
				x="constants.Video.FrameRate.FR" + fps
				videoFps = eval(x)
				print(self.gpControlSet(constants.Video.FRAME_RATE,videoFps))
		elif self.whichCam() == "auth":
			if res == "4k":
				print(self.sendCamera(constants.Hero3Commands.VIDEO_RESOLUTION,"06"))
			elif res == "4K_Widescreen":
				print(self.sendCamera(constants.Hero3Commands.VIDEO_RESOLUTION,"08"))
			elif res == "2kCin":
				print(self.sendCamera(constants.Hero3Commands.VIDEO_RESOLUTION,"07"))
			elif res == "2_7k":
				print(self.sendCamera(constants.Hero3Commands.VIDEO_RESOLUTION,"05"))
			elif res == "1440p":
				print(self.sendCamera(constants.Hero3Commands.VIDEO_RESOLUTION,"04"))
			elif res == "1080p":
				print(self.sendCamera(constants.Hero3Commands.VIDEO_RESOLUTION,"03"))
			elif res == "960p":
				print(self.sendCamera(constants.Hero3Commands.VIDEO_RESOLUTION,"02"))
			elif res == "720p":
				print(self.sendCamera(constants.Hero3Commands.VIDEO_RESOLUTION,"01"))
			elif res == "480p":
				print(self.sendCamera(constants.Hero3Commands.VIDEO_RESOLUTION,"00"))
			if fps != "none":
				x="constants.Hero3Commands.FrameRate.FPS" + fps
				videoFps = eval(x)
				print(self.sendCamera(constants.Hero3Commands.FRAME_RATE,videoFps))
	def take_photo(self,timer=1):
		self.mode(constants.Mode.PhotoMode)
		time.sleep(timer)
		self.shutter(constants.start)
		ready=int(self.getStatus(constants.Status.Status, constants.Status.STATUS.IsBusy))
		while ready==1:
				ready=int(self.getStatus(constants.Status.Status, constants.Status.STATUS.IsBusy))
		return self.getMedia()
	def shoot_video(self, duration=0):
		self.mode(constants.Mode.VideoMode)
		self.shutter(constants.start)
		if duration != 0 and duration > 2:
			time.sleep(duration)
			self.shutter(constants.stop)
			ready=int(self.getStatus(constants.Status.Status, constants.Status.STATUS.IsBusy))
			while ready==1:
				ready=int(self.getStatus(constants.Status.Status, constants.Status.STATUS.IsBusy))
			return self.getMedia()
	def getMedia(self):
		folder = ""
		file_lo = ""
		try:
			raw_data = urllib.request.urlopen('http://10.5.5.9:8080/gp/gpMediaList').read().decode('utf-8')
			json_parse = json.loads(raw_data)
			for i in json_parse['media']:
				folder=i['d']
			for i in json_parse['media']:
				for i2 in i['fs']:
					file_lo = i2['n']
			return "http://10.5.5.9:8080/videos/DCIM/" + folder + "/" + file_lo
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def getMediaInfo(self, option):
		folder = ""
		file = ""
		size = ""
		try:
			raw_data = urllib.request.urlopen('http://10.5.5.9:8080/gp/gpMediaList').read().decode('utf-8')
			json_parse = json.loads(raw_data)
			for i in json_parse['media']:
				folder=i['d']
			for i in json_parse['media']:
				for i2 in i['fs']:
					file = i2['n']
					size = i2['s']
			if option == "folder":
				return folder
			elif option == "file":
				return file
			elif option == "size":
				return size
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def listMedia(self):
		try:
			raw_data = urllib.request.urlopen('http://10.5.5.9:8080/gp/gpMediaList').read().decode('utf-8')
			parsed_resp=json.loads(raw_data)
			print(json.dumps(parsed_resp, indent=2, sort_keys=True))
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def syncTime(self):
		now = datetime.datetime.now()
		year=str(now.year)[-2:]
		datestr_year=format(int(year), 'x')
		datestr_month=format(now.month, 'x')
		datestr_day=format(now.day, 'x')
		datestr_hour=format(now.hour, 'x')
		datestr_min=format(now.minute, 'x')
		datestr_sec=format(now.second, 'x')
		datestr=str("%" + str(datestr_year)+"%"+str(datestr_month)+"%"+str(datestr_day)+"%"+str(datestr_hour)+"%"+str(datestr_min)+"%"+str(datestr_sec))
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand('setup/date_time?p=' + datestr))
		else:
			print(self.sendCamera("TM",datestr))
	def downloadLastMedia(self):
		urllib.request.urlretrieve(self.getMedia(), self.getMediaInfo("file"))
	def livestream(self,option):
		if option == "start":
			if self.whichCam() == "gpcontrol":
				print(self.gpControlExecute('p1=gpStream&a1=proto_v2&c1=restart'))
			else:
				print(self.sendCamera("PV","02"))
		if option == "stop":
			if self.whichCam() == "gpcontrol":
				print(self.gpControlExecute('p1=gpStream&a1=proto_v2&c1=stop'))
			else:
				print(self.sendCamera("PV","00"))
	def parse_value(self, param,value):
		if param=="mode":		
			if value == 0:
				return "Video"
			if value == 1:
				return "Photo"
			if value == 2:
				return "Multi-Shot"	
		if param == "sub_mode":
			if self.getStatus(constants.Status.Status, constants.Status.STATUS.Mode) == 0:
				if value ==  0:
					return "Video"
				if value ==  1:
					return "TimeLapse Video"
				if value ==  2:
					return "Video+Photo"
				if value ==  3:
					return "Looping"
		
			if self.getStatus(constants.Status.Status, constants.Status.STATUS.Mode) == 1:
				if value ==  0:
					return "Single Pic"
				if value ==  1:
					return "Burst"
				if value ==  2:
					return "NightPhoto"
		
			if self.getStatus(constants.Status.Status, constants.Status.STATUS.Mode) == 2:
				if value ==  0:
					return "Burst"
				if value ==  1:
					return "TimeLapse"
				if value ==  2:
					return "Night lapse"
						
				
		if param == "recording":
			if value ==  0:
				return "Not recording - standby"
			if value ==  1:
				return "RECORDING!"
				
		if param == "battery":
			if value == 0:
				return "Nearly Empty"
			if value == 1:
				return "LOW"
			if value == 2:
				return "Halfway"
			if value == 3:
				return "Full"
			if value == 4:
				return "Charging"
				
		if param == "video_left":
			return str(time.strftime("%H:%M:%S", time.gmtime(value)))
		if param == "rem_space":
			return str(round(value/1000000, 2))
		if param == "video_res":		
			if value == 1:
				return "4k"
			if value == 2:
				return "4kSV"
			if value == 4:
				return "2k"
			if value == 5:
				return "2kSV"
			if value == 6:
				return "2k4by3"
			if value == 7:
				return "1440p"
			if value == 8:
				return "1080pSV"
			if value == 9:
				return "1080p"
			if value == 10:
				return "960p"
			if value == 11:
				return "720pSV"
			if value == 12:
				return "720p"
			if value == 13:
				return "480p"
		if param == "video_fr":
			if value == 0:
				return "240"
			if value == 1:
				return "120"
			if value == 2:
				return "100"
			if value == 5:
				return "60"
			if value == 6:
				return "50"
			if value == 7:
				return "48"
			if value == 8:
				return "30"
			if value == 9:
				return "25"
			if value == 10:
				return "24"
	def overview(self):
		print("camera overview")
		print("current mode: " + "" + self.parse_value("mode", self.getStatus(constants.Status.Status, constants.Status.STATUS.Mode)))
		print("current submode: " + "" + self.parse_value("sub_mode",self.getStatus(constants.Status.Status, constants.Status.STATUS.SubMode)))
		print("current video resolution: " + "" + self.parse_value("video_res",self.getStatus(constants.Status.Settings, constants.Video.RESOLUTION)))
		print("current video framerate: " + "" + self.parse_value("video_fr",self.getStatus(constants.Status.Settings, constants.Video.FRAME_RATE)))
		print("pictures taken: " + "" + str(self.getStatus(constants.Status.Status, constants.Status.STATUS.PhotosTaken)))
		print("videos taken: ",  "" + str(self.getStatus(constants.Status.Status, constants.Status.STATUS.VideosTaken)))
		print("videos left: " + "" + self.parse_value("video_left",self.getStatus(constants.Status.Status, constants.Status.STATUS.RemVideoTime)))
		print("pictures left: " + "" + str(self.getStatus(constants.Status.Status, constants.Status.STATUS.RemPhotos)))
		print("battery left: " + "" + self.parse_value("battery",self.getStatus(constants.Status.Status, constants.Status.STATUS.BatteryLevel)))
		print("space left in sd (GBs): " + "" + self.parse_value("rem_space",self.getStatus(constants.Status.Status, constants.Status.STATUS.RemainingSpace)))
		print("camera SSID: " + "" + str(self.getStatus(constants.Status.Status, constants.Status.STATUS.CamName)))
		print("Is Recording: " + "" + self.parse_value("recording",self.getStatus(constants.Status.Status, constants.Status.STATUS.IsRecording)))
		print("Clients connected: " + "" + str(self.getStatus(constants.Status.Status, constants.Status.STATUS.IsConnected)))
		print("camera model: " + "" + self.infoCamera(constants.Camera.Name))
		print("camera ssid name: " + "" + self.infoCamera(constants.Camera.SSID))
		print("firmware version: " + "" + self.infoCamera(constants.Camera.Firmware))
		print("serial number: " + "" + self.infoCamera(constants.Camera.SerialNumber))
