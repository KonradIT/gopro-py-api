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
import http
import math
import base64
import sys
import ssl


class GoPro:
	def prepare_gpcontrol(self):
		try:
			response_raw = urllib.request.urlopen('http://' + self.ip_addr + '/gp/gpControl', timeout=5).read().decode('utf8')
			jsondata=json.loads(response_raw)
			response=jsondata["info"]["firmware_version"]
			if "HX" in response: #Only session cameras.
				connectedStatus=False
				while connectedStatus == False:
					req=urllib.request.urlopen("http://" + self.ip_addr + "/gp/gpControl/status")
					data = req.read()
					encoding = req.info().get_content_charset('utf-8')
					json_data = json.loads(data.decode(encoding))
					#print(json_data["status"]["31"])
					if json_data["status"]["31"] >= 1:
						connectedStatus=True
		except (HTTPError, URLError) as error:
			self.prepare_gpcontrol()
		except timeout:
			self.prepare_gpcontrol()
		
		print("Camera successfully connected!")
	def __init__(self, camera="detect", ip_address="10.5.5.9", mac_address="AA:BB:CC:DD:EE:FF"):
		if sys.version_info[0] < 3:
			print("Needs Python v3, run again on a virtualenv or install Python 3")
			exit()
		self.ip_addr = ip_address
		self._camera=""
		self._mac_address=mac_address
		try:
			from getmac import get_mac_address
			self._mac_address = get_mac_address(ip="10.5.5.9")
		except ImportError:
			self._mac_address=mac_address
		if camera == "detect":
			self._camera = self.whichCam()
		elif camera == "startpair":
			self.pair()
		else:
			if camera == "auth" or camera == "HERO3" or camera == "HERO3+" or camera == "HERO2":
				self.power_on_auth()
				time.sleep(2)
				self._camera="auth"
			else:
				self._camera="gpcontrol"
				self.power_on(self._mac_address)
				self.prepare_gpcontrol()
			print("Connected to " + self.ip_addr)
	def __str__(self):
		return str(self.infoCamera())
	def KeepAlive(self):
		"""Sends keep alive packet"""
		while True:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.sendto("_GPHD_:0:0:2:0.000000\n".encode(), (self.ip_addr, 8554))
			time.sleep(2500/1000)
	def getPassword(self):
		"""Gets password from Hero3, Hero3+ cameras"""
		try:
			PASSWORD = urllib.request.urlopen('http://' + self.ip_addr + '/bacpac/sd', timeout=5).read()
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
		"""sends Parameter and value to gpControl/setting"""
		try:
			return urllib.request.urlopen('http://' + self.ip_addr + '/gp/gpControl/setting/' + param + '/' + value, timeout=5).read().decode('utf-8')
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	
	def gpControlCommand(self, param):
		"""sends Parameter gpControl/command"""
		try:
			return urllib.request.urlopen('http://' + self.ip_addr + '/gp/gpControl/command/' + param, timeout=5).read().decode('utf-8')
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def gpControlExecute(self, param):
		"""sends Parameter to gpControl/execute"""
		try:
			return urllib.request.urlopen('http://' + self.ip_addr + '/gp/gpControl/execute?' + param, timeout=5).read().decode('utf-8')
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def sendCamera(self, param,value=""):
		"""sends Parameter and value to 10.5.5.9/camera/"""
		value_notempty = ""
		if not value == "":
			if len(value) == 2:
				value_notempty=str('&p=%' + value)
			else:
				value_notempty=str('&p=' + value)
		#sends parameter and value to /camera/
		try:
			urllib.request.urlopen('http://' + self.ip_addr + '/camera/' + param + '?t=' + self.getPassword() + value_notempty, timeout=5).read()
		except (HTTPError, URLError) as error:
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")	
	def sendBacpac(self, param,value):
		"""sends Parameter and value to 10.5.5.9/camera/"""
		value_notempty = ""
		if value:
			value_notempty=str('&p=%' + value)
		try:
			urllib.request.urlopen('http://' + self.ip_addr + '/bacpac/' + param + '?t=' + self.getPassword() + value_notempty, timeout=5).read()
		except (HTTPError, URLError) as error:
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def whichCam(self):
		""" This returns what type of camera is currently connected.
		 - gpcontrol: HERO4 Black and Silver, HERO5 Black and Session, HERO Session (formally known as HERO4 Session), HERO+ LCD, HERO+.
		 - auth: HERO2 with WiFi BacPac, HERO3 Black/Silver/White, HERO3+ Black and Silver. """
		if self._camera != "":
			return self._camera
		else:
			try:
				response_raw = urllib.request.urlopen('http://' + self.ip_addr + '/gp/gpControl', timeout=5).read().decode('utf8')
				jsondata=json.loads(response_raw)
				response=jsondata["info"]["firmware_version"]
				response_parsed=3
				exception_found = False
				if "HD" in response:
					response_parsed=response.split("HD")[1][0]
				exceptions=["HX","FS","HD3.02","H18"]
				for camera in exceptions:
					if camera in response:
						exception_found = True
						break
				if int(response_parsed) > 3 or exception_found: #HD4 (Hero4), HD5 (Hero5), HD6 (Hero6)... Exceptions: HX (HeroSession), FS (Fusion), HD3.02 (Hero+), H18 (Hero 2018)
					print(jsondata["info"]["model_name"] + "\n" + jsondata["info"]["firmware_version"])
					self.prepare_gpcontrol()
					self._camera="gpcontrol"
				else:
					response = urllib.request.urlopen('http://' + self.ip_addr + '/camera/cv',timeout=5).read()
					if b"Hero3" in response: #should detect HERO3/3+
						self._camera="auth"
			except (HTTPError, URLError) as error:
				try:
					response = urllib.request.urlopen('http://' + self.ip_addr + '/camera/cv',timeout=5).read()
					if b"Hero3" in response: #should detect HERO3/3+
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
				self.power_on(self._mac_address)
				time.sleep(5)
				response = urllib.request.urlopen('http://' + self.ip_addr + '/camera/cv',timeout=5).read()
				if b"Hero3" in response:
					self._camera="auth"
				else:
					self.prepare_gpcontrol()
			except http.client.HTTPException as httperror:
				print(httperror)
				self.power_on_auth()
				#Definitively HERO3+ and below.
				time.sleep(2)
				response = urllib.request.urlopen('http://' + self.ip_addr + '/camera/cv',timeout=5).read()
				if b"Hero3" in response:
					print("HERO3/3+")
				self._camera="auth"
			return self._camera
	
	
	def getStatus(self, param, value=""):
		"""This returns a status message based on param (status/setting) and value (numeric)"""
		if self.whichCam() == "gpcontrol":
			try:
				req=urllib.request.urlopen("http://" + self.ip_addr + "/gp/gpControl/status", timeout=5)
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
		else:
			response = urllib.request.urlopen("http://" + self.ip_addr + "/camera/sx?t=" + self.getPassword(), timeout=5).read()
			response_hex = str(bytes.decode(base64.b16encode(response), 'utf-8'))
			return str(response_hex[param[0]:param[1]])

	def getStatusRaw(self):
		"""Delivers raw status message"""
		if self.whichCam() == "gpcontrol":
			try:
				return urllib.request.urlopen("http://" + self.ip_addr + "/gp/gpControl/status", timeout=5).read().decode('utf-8')
			except (HTTPError, URLError) as error:
				return ""
				print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
			except timeout:
				return ""
				print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		elif self.whichCam() == "auth":
			try:
				return urllib.request.urlopen("http://" + self.ip_addr + "/camera/sx?t=" + self.getPassword(), timeout=5).read()
			except (HTTPError, URLError) as error:
				return ""
				print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
			except timeout:
				return ""
				print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		else:
			print("Error, camera not defined.")
	def changeWiFiSettings(self, ssid, password):
		"""Changes ssid and passwod of Hero4 camera"""
		if self.whichCam() == "gpcontrol":
			self.gpControlCommand("wireless/ap/ssid?ssid=" + ssid + "&pw=" + password)
			print("Disconnecting")
			exit()
	def infoCamera(self, option=""):
		"""Gets camera info, such as mac address and firmware version. See constants.Camera for possible options."""
		if self.whichCam() == "gpcontrol":
			try:
				info=urllib.request.urlopen('http://' + self.ip_addr + '/gp/gpControl', timeout=5)
				data = info.read()
				encoding = info.info().get_content_charset('utf-8')

				parse_read = json.loads(data.decode(encoding))
				parsed_info = ""
				if option == "":
					parsed_info = parse_read["info"]
				else:
					parsed_info = parse_read["info"][option]
				return parsed_info
			except (HTTPError, URLError) as error:
				return ""
				print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
			except timeout:
				return ""
				print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		elif self.whichCam() == "auth":
			if option == "model_name" or option == "firmware_version":
				try:
					info=urllib.request.urlopen('http://' + self.ip_addr + '/camera/cv', timeout=5)
					data = info.read()
					parsed=re.sub(r'\W+', '', str(data))
					print(parsed)
					return parsed #an error is raised in take_photo if no value is returned
				except (HTTPError, URLError) as error:
					return ""
					print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
				except timeout:
					return ""
					print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
			if option == "ssid":
				try:
					info=urllib.request.urlopen('http://' + self.ip_addr + '/bacpac/cv', timeout=5)
					data = info.read()
					parsed=re.sub(r'\W+', '', str(data))
					print(parsed)
					return parsed #an error is raised in take_photo if no value is returned
				except (HTTPError, URLError) as error:
					return ""
					print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
				except timeout:
					return ""
					print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		else:
			print("Error, camera not defined.")
	
	def shutter(self,param):
		"""Starts/stop video or timelapse recording, pass constants.start or constants.stop as value in param"""
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("shutter?p=" + param))
		else:
			if len(param) == 1:
				param = "0" + param
			self.sendBacpac("SH",param)
	
	
	def mode(self, mode, submode="0"):
		"""Changes mode of the camera. See constants.Mode and constants.Mode.SubMode for sub-modes."""
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("sub_mode?mode=" + mode + "&sub_mode=" + submode))
		else:
			if len(mode) == 1:
				mode = "0" + mode
			self.sendCamera("CM",mode)
	def delete(self, option):
		"""Deletes media. "last", "all" or an integer are accepted values for option"""
		if self.whichCam() == "gpcontrol":
			if isinstance(option, int): #This allows you to delete x number of files backwards. Will delete a timelapse/burst entirely as its interpreted as a single file.
				for _ in range(option):
					print(self.gpControlCommand("storage/delete/" + "last"))
			else:
				print(self.gpControlCommand("storage/delete/" + option))
		else:
			if isinstance(option, int) == True:
				for _ in range(option):
					print(self.sendCamera("DL"))
			else:
				if option == "last":
					print(self.sendCamera("DL"))
				if option == "all":
					print(self.sendCamera("DA"))
	def deleteFile(self, folder,file):
		"""Deletes a file. Pass folder and file as parameters."""
		if folder.startswith("http://" + self.ip_addr):
			folder, file = self.getInfoFromURL(folder)
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("storage/delete?p=" + folder + "/" + file))
		else:
			print(self.sendCamera("DF","/"+folder+"/"+file))
	def locate(self, param):
		"""Starts or stops locating (beeps camera)"""
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("system/locate?p=" + param))
		else:
			print(self.sendCamera("LL","0"+param))
				
	def hilight(self):
		"""Tags a hilight in the video"""
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("storage/tag_moment"))
		else:
			print("Not supported.")
	
	def power_off(self):
		"""Sends power off command"""
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("system/sleep"))
		else:
			print(self.sendBacpac("PW","00"))
			
	def power_on(self,_mac_address=""):
		"""Sends power on command. Mac address might need to be defined"""
		print("Waking up...")
		mac_address=_mac_address
		if mac_address is None:
			mac_address = "AA:BB:CC:DD:EE:FF"
		else:
			mac_address = str(mac_address)
			if len(mac_address) == 12:
				pass
			elif len(mac_address) == 17:
				sep = mac_address[2]
				mac_address = mac_address.replace(sep, '')

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		data = bytes('FFFFFFFFFFFF' + mac_address * 16, 'utf-8')
		message = b''
		for i in range(0, len(data), 2):
				message += struct.pack(b'B', int(data[i: i + 2], 16))
		sock.sendto(message, (self.ip_addr, 9))
		#Fallback for HERO5
		sock.sendto(message, (self.ip_addr, 7))
	def pair(self, usepin=True):
		"""This is a pairing procedure needed for HERO4 and HERO5 cameras. When those type GoPro camera are purchased the GoPro Mobile app needs an authentication code when pairing the camera to a mobile device for the first time. 
		The code is useless afterwards. This function will pair your GoPro to the machine without the need of using the mobile app -- at all. """
		if usepin == False:
			paired_resp = ""
			while "{}" not in paired_resp:
				paired_resp = urllib.request.urlopen('http://' + self.ip_addr + '/gp/gpControl/command/wireless/pair/complete?success=1&deviceName=' + socket.gethostname(), timeout=5).read().decode('utf8')
			print("Paired")
			return
		else:
			print("Make sure your GoPro camera is in pairing mode!\nGo to settings > Wifi > PAIR > GoProApp to start pairing.\nThen connect to it, the ssid name should be GOPRO-XXXX/GPXXXXX/GOPRO-BP-XXXX and the password is goprohero")
			code=str(input("Enter pairing code: "))
			_context = ssl._create_unverified_context()
			ssl._create_default_https_context = ssl._create_unverified_context
			response_raw = urllib.request.urlopen('https://' + self.ip_addr + '/gpPair?c=start&pin=' + code + '&mode=0', context=_context).read().decode('utf8')
			print(response_raw)
			response_raw = urllib.request.urlopen('https://' + self.ip_addr + '/gpPair?c=finish&pin=' + code + '&mode=0', context=_context).read().decode('utf8')
			print(response_raw)
			wifi_ssid=input("Enter your desired camera wifi ssid name: ")
			wifi_pass=input("Enter new wifi password: ")
			self.gpControlCommand("wireless/ap/ssid?ssid=" + wifi_ssid + "&pw=" + wifi_pass)
			print("Connect now!")
	def power_on_auth(self):
		"""Sends power on command to Hero 3/3+ cameras"""
		print(self.sendBacpac("PW","01"))
	def video_settings(self, res, fps="none"):
		"""Change video resolution and FPS
		See constants.Video.Resolution"""
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
		"""Takes a photo. Set timer to an integer to set a wait time"""
		if "HERO5 Black" in self.infoCamera(constants.Camera.Name) or "HERO6" in self.infoCamera(constants.Camera.Name):
			self.mode(constants.Mode.PhotoMode, constants.Mode.SubMode.Photo.Single_H5)
		else:
			self.mode(constants.Mode.PhotoMode)
		if timer > 1:
				print("wait " + str(timer) + " seconds.")
		time.sleep(timer)
		self.shutter(constants.start)
		
		if self.whichCam() == "gpcontrol":
			ready=int(self.getStatus(constants.Status.Status, constants.Status.STATUS.IsBusy))
			while ready==1:
					ready=int(self.getStatus(constants.Status.Status, constants.Status.STATUS.IsBusy))
			return self.getMedia()
		elif self.whichCam() == "auth":
			ready=str(self.getStatus(constants.Hero3Status.IsRecording))
			while ready=="01":
					ready=str(self.getStatus(constants.Hero3Status.IsRecording))
			return self.getMedia()
	def shoot_video(self, duration=0):
		"""Shoots a video, if duration is 0 it will not stop the video, set duration to an integer to set the video duration."""
		self.mode(constants.Mode.VideoMode)
		time.sleep(1)
		self.shutter(constants.start)
		if duration != 0 and duration > 2:
			time.sleep(duration)
			self.shutter(constants.stop)
			if self.whichCam() == "gpcontrol":
				ready=int(self.getStatus(constants.Status.Status, constants.Status.STATUS.IsBusy))
				while ready==1:
					ready=int(self.getStatus(constants.Status.Status, constants.Status.STATUS.IsBusy))
				return self.getMedia()
			elif self.whichCam() == "auth":
				ready=str(self.getStatus(constants.Hero3Status.IsRecording))
				while ready=="01":
						ready=str(self.getStatus(constants.Hero3Status.IsRecording))
				return self.getMedia()

	def syncTime(self):
		"""Sets time and date to computer's time and date"""
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
	def reset(self, r):
		"""Resets video/photo/multishot protune values"""
		self.gpControlCommand(r + "/protune/reset")
	def setZoom(self, zoomLevel):
		"""Sets camera zoom (Hero6/Hero7), zoomLevel is an integer"""
		if zoomLevel >= 0 and zoomLevel <= 100:
			self.gpControlCommand("digital_zoom?range_pcnt=" + str(zoomLevel))
	def getMedia(self):
		"""Returns last media URL"""
		if "FS" in self.infoCamera(constants.Camera.Firmware):
			return self.getMediaFusion()
		else:
			folder = ""
			file_lo = ""
			try:
				raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaList').read().decode('utf-8')
				json_parse = json.loads(raw_data)
				for i in json_parse['media']:
					folder=i['d']
				for i in json_parse['media']:
					for i2 in i['fs']:
						file_lo = i2['n']
				return "http://" + self.ip_addr + ":8080/videos/DCIM/" + folder + "/" + file_lo
			except (HTTPError, URLError) as error:
				return ""
				print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
			except timeout:
				return ""
				print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def getMediaFusion(self):
		folder_1=""
		folder_2=""
		file_1 = ""
		file_2 = ""
		try:
			raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaListEx').read().decode('utf-8')
			json_parse = json.loads(raw_data)
			for i in json_parse[0]['media']:
				folder_1=i['d']
				if "GBACK" in i['d']:
					folder_2=i['d'].replace("GBACK","GFRNT")
				else:
					folder_2=i['d'].replace("GFRNT","GBACK")
			for mediaitem in json_parse[0]['media']:
				if mediaitem["d"] == folder_1:
					for mediaitem2 in mediaitem["fs"]:
						file_1 = mediaitem2["n"]
			for mediaitem in json_parse[1]['media']:
				if mediaitem["d"] == folder_2:
					for mediaitem2 in mediaitem["fs"]:
						file_2 = mediaitem2["n"]

			return ["http://" + self.ip_addr + ":8080/videos/DCIM/" + folder_1 + "/" + file_1, "http://" + self.ip_addr + ":8080/videos2/DCIM/" + folder_2 + "/" + file_2]
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def getMediaInfo(self, option):
		"""Returns an array of the last media, both front and back URLs"""
		folder = ""
		file = ""
		size = ""
		try:

			
			if "FS" in self.infoCamera(constants.Camera.Firmware):
				folder_1=""
				folder_2=""
				file_1=""
				file_2=""
				size_1=""
				size_2=""
				raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaListEx').read().decode('utf-8')
				json_parse = json.loads(raw_data)
				for i in json_parse[0]['media']:
					folder_1=i['d']
					if "GBACK" in i['d']:
						folder_2=i['d'].replace("GBACK","GFRNT")
					else:
						folder_2=i['d'].replace("GFRNT","GBACK")
				for mediaitem in json_parse[0]['media']:
					if mediaitem["d"] == folder_1:
						for mediaitem2 in mediaitem["fs"]:
							file_1 = mediaitem2["n"]
							size_1 = mediaitem2["s"]

				for mediaitem in json_parse[1]['media']:
					if mediaitem["d"] == folder_2:
						for mediaitem2 in mediaitem["fs"]:
							file_2 = mediaitem2["n"]
							size_2 = mediaitem2["s"]
				if option == "folder":
					return [folder_1,folder_2]
				elif option == "file":
					return  [file_1,file_2]
				elif option == "size":
					return [self.parse_value("media_size", int(size_1)), self.parse_value("media_size", int(size_2))]
			else:
				raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaList').read().decode('utf-8')
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
					return self.parse_value("media_size", int(size))
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def listMedia(self, format=False, media_array=False):
		"""Lists media on SD card
		format = (True/False) - Sets formatting
		media_array = (True/False) - returns an array"""
		try:
			if format == False:
				if "FS" in self.infoCamera(constants.Camera.Firmware):
					raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaListEx').read().decode('utf-8')
					parsed_resp=json.loads(raw_data)
					return json.dumps(parsed_resp, indent=2, sort_keys=True)
				else:
					raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaList').read().decode('utf-8')
					parsed_resp=json.loads(raw_data)
					return json.dumps(parsed_resp, indent=2, sort_keys=True)
			else:
				if media_array == True:
					media=[]
					if "FS" in self.infoCamera(constants.Camera.Firmware):
						raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaListEx').read().decode('utf-8')
						json_parse = json.loads(raw_data)						
						medialength=len(json_parse)
						for i in range(medialength):
							for folder in json_parse[i]['media']:
								for item in folder['fs']:
									media.append([folder['d'],item['n'], item['s'], item['mod']])
					else:
						raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaList').read().decode('utf-8')
						json_parse = json.loads(raw_data)
						for i in json_parse['media']:
							for i2 in i['fs']:
								media.append([i['d'], i2['n'], i2['s'], i2['mod']])
					return media
				else:
					if "FS" in self.infoCamera(constants.Camera.Firmware):
						raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaListEx').read().decode('utf-8')
						json_parse = json.loads(raw_data)
						medialength=len(json_parse)
						for i in range(medialength):
							for folder in json_parse[i]['media']:
								for item in folder['fs']:
									print(item['n'])
					else:
						raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaList').read().decode('utf-8')
						json_parse = json.loads(raw_data)
						medialength=len(json_parse)
						for i in range(medialength):
							for folder in json_parse['media']:
								for item in folder['fs']:
									print(item['n'])
		except (HTTPError, URLError) as error:
			return ""
			print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
		except timeout:
			return ""
			print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	## 
	## Misc media utils
	##
	def IsRecording(self):
		"""Returns either 0 or 1 if the camera is recording or not."""
		if self.whichCam() == "gpcontrol":
			return self.getStatus(constants.Status.Status, constants.Status.STATUS.IsRecording)
		elif self.whichCam() == "auth":
			if self.getStatus(constants.Hero3Status.IsRecording) == '00':
 				return 0
			else:
				return 1
	def getInfoFromURL(self, url):
		"""Gets information from Media URL."""
		media=[]
		media.append(url.replace('http://' + self.ip_addr + ':8080/videos/DCIM/','').replace('/','-').rsplit('-', 1)[0])
		media.append(url.replace('http://' + self.ip_addr + ':8080/videos/DCIM/','').replace('/','-').rsplit('-', 1)[1])
		return media

	##
	## Downloading media functions
	##
	def downloadMultiShot(self, path=""):
		"""Downloads a multi-shot sequence."""
		if path == "":
			path = self.getMedia()
			folder = self.getInfoFromURL(path)[0]
			filename = self.getInfoFromURL(path)[1]
			arr = json.loads(self.listMedia())
			lower_bound = 0
			high_bound = 0
			for i in arr['media']:
				for i2 in i['fs']:
					if i['d'] == folder:
						for i in arr['media']:
							for i2 in i['fs']:
								if i2['n'] == filename:
									lower_bound = i2["b"]
									high_bound = i2["l"]
			for i in range(int(high_bound) - int(lower_bound)+1):
				f = filename[:4] + str(int(lower_bound) + i) + ".JPG"
				self.downloadMedia(folder, f)
		else:
			folder = self.getInfoFromURL(path)[0]
			filename = self.getInfoFromURL(path)[1]
			arr = json.loads(self.listMedia())
			lower_bound = 0
			high_bound = 0
			for i in arr['media']:
				for i2 in i['fs']:
					if i['d'] == folder:
						for i in arr['media']:
							for i2 in i['fs']:
								if i2['n'] == filename:
									lower_bound = i2["b"]
									high_bound = i2["l"]
			for i in range(int(high_bound) - int(lower_bound)+1):
				f = filename[:4] + str(int(lower_bound) + i) + ".JPG"
				self.downloadMedia(folder, f)
	def downloadLastMedia(self, path="", custom_filename=""):
		"""Downloads last media taken, set custom_filename to download to that filename"""
		if self.IsRecording() == 0:
			if path == "":
				if "FS" in self.infoCamera(constants.Camera.Firmware):
					print("filename: " + self.getMediaInfo("file")[0] + "\nsize: " + self.getMediaInfo("size")[0])
					print("filename: " + self.getMediaInfo("file") [1]+ "\nsize: " + self.getMediaInfo("size")[1])
					urllib.request.urlretrieve(self.getMedia()[0], self.getMediaInfo("folder")[0]+self.getMediaInfo("file")[0])
					urllib.request.urlretrieve(self.getMedia()[1], self.getMediaInfo("folder")[1]+self.getMediaInfo("file")[1])
				else:
					print("filename: " + self.getMediaInfo("file") + "\nsize: " + self.getMediaInfo("size"))
					if custom_filename == "":
						custom_filename = self.getMediaInfo("folder")+"-"+self.getMediaInfo("file")
					urllib.request.urlretrieve(self.getMedia(), custom_filename)
			else:
				print("filename: " + self.getInfoFromURL(path)[1])
				filename = ""
				if custom_filename == "":
					filename = self.getInfoFromURL(path)[0]+"-"+self.getInfoFromURL(path)[1]
				else:
					filename = custom_filename
				urllib.request.urlretrieve(path, filename)
		else:
			print("Not supported while recording or processing media.")
	def downloadLastRawPhoto(self, custom_filename=""):
		"""Downloads last media taken, set custom_filename to download to that filename"""
		if self.IsRecording() == 0:
			if "FS" in self.infoCamera(constants.Camera.Firmware):
				if self.getMediaInfo("file")[0].endswith("JPG"):
					print("filename: " + self.getMediaInfo("file")[0].replace("JPG","GPR") + "\nsize: " + self.getMediaInfo("size")[0])
					print("filename: " + self.getMediaInfo("file") [1].replace("JPG","GPR")+ "\nsize: " + self.getMediaInfo("size")[1])
					urllib.request.urlretrieve(self.getMedia()[0], self.getMediaInfo("folder")[1]+self.getMediaInfo("file")[0])
					urllib.request.urlretrieve(self.getMedia()[1], self.getMediaInfo("folder")[1]+self.getMediaInfo("file")[1])
			else:
				if self.getMediaInfo("file").endswith("JPG"):
					print("filename: " + self.getMediaInfo("file").replace("JPG","GPR") + "\nsize: " + self.getMediaInfo("size"))
					if custom_filename == "":
						custom_filename = self.getMediaInfo("folder")+"-"+self.getMediaInfo("file").replace("JPG","GPR")
					GPRURL=self.getMedia().replace("JPG","GPR")
					urllib.request.urlretrieve(GPRURL, custom_filename)
		else:
			print("Not supported while recording or processing media.")
	def downloadMedia(self, folder, file, custom_filename=""):
		"""Downloads specific folder and filename"""
		if self.IsRecording() == 0:
			print("filename: " + file)
			filename = ""
			if custom_filename == "":
				filename = file
			else:
				filename = custom_filename
			try:
				if "FS" in self.infoCamera(constants.Camera.Firmware):
					if "GFRNT" in folder:
						urllib.request.urlretrieve("http://" + self.ip_addr + ":8080/videos2/DCIM/" + folder + "/" + file, filename)
				urllib.request.urlretrieve("http://" + self.ip_addr + ":8080/videos/DCIM/" + folder + "/" + file, filename)
			except (HTTPError, URLError) as error:
				print("ERROR: " + str(error))
		else:
			print("Not supported while recording or processing media.")

	def downloadRawPhoto(self, folder, file, custom_filename=""):
		"""Downloads specific folder and filename"""
		if self.IsRecording() == 0:
			file=file.replace("JPG","GPR")
			print("filename: " + file)
			filename = ""
			if custom_filename == "":
				filename = file
			else:
				filename = custom_filename
			try:
				if "FS" in self.infoCamera(constants.Camera.Firmware):
					if "GFRNT" in folder:
						urllib.request.urlretrieve("http://" + self.ip_addr + ":8080/videos2/DCIM/" + folder + "/" + file, filename)
				urllib.request.urlretrieve("http://" + self.ip_addr + ":8080/videos/DCIM/" + folder + "/" + file, filename)
			except (HTTPError, URLError) as error:
				print("ERROR: " + str(error))
		else:
			print("Not supported while recording or processing media.")
	def downloadAll(self, option=""):
		"""Download all media on camera"""
		media_stash=[]
		if option == "":
			try:
				folder = ""
				file = ""
				raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaList').read().decode('utf-8')
				json_parse = json.loads(raw_data)
				for i in json_parse['media']:
					folder=i['d']
					for i2 in i['fs']:
						file = i2['n']
						self.downloadMedia(folder,file, folder+"-"+file)
						media_stash.append(file)
				return media_stash
			except (HTTPError, URLError) as error:
				print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
			except timeout:
				print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		if option == "videos":
			try:
				folder = ""
				file = ""
				raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaList').read().decode('utf-8')
				json_parse = json.loads(raw_data)
				for i in json_parse['media']:
					folder=i['d']
					for i2 in i['fs']:
						file = i2['n']
						if file.endswith("MP4"):
							self.downloadMedia(folder,file, folder+"-"+file)
							media_stash.append(file)
				return media_stash
			except (HTTPError, URLError) as error:
				print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
			except timeout:
				print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
		if option == "photos":
			try:
				folder = ""
				file = ""
				raw_data = urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaList').read().decode('utf-8')
				json_parse = json.loads(raw_data)
				for i in json_parse['media']:
					folder=i['d']
					for i2 in i['fs']:
						file = i2['n']
						if file.endswith("JPG"):
							self.downloadMedia(folder,file, folder+"-"+file)
							media_stash.append(file)
				return media_stash
			except (HTTPError, URLError) as error:
				print("Error code:" + str(error.code) + "\nMake sure the connection to the WiFi camera is still active.")
			except timeout:
				print("HTTP Timeout\nMake sure the connection to the WiFi camera is still active.")
	def downloadLowRes(self, path="", custom_filename = ""):
		"""Downloads the low-resolution video"""
		if self.IsRecording() == 0:
			if path == "":
				url=""
				if "FS" in self.infoCamera(constants.Camera.Firmware):
					url=self.getMedia()[0]
				else:
					url=self.getMedia()
				lowres_url=""
				lowres_filename=""
				if url.endswith("MP4"):
					lowres_url=url.replace('MP4', 'LRV')
					if "GH" in lowres_url:
						lowres_url=lowres_url.replace("GH","GL")
					lowres_filename=""
					if "FS" in self.infoCamera(constants.Camera.Firmware):
						lowres_filename = "LOWRES"+self.getMediaInfo("folder")[0]+"-"+self.getMediaInfo("file")[0]
					else:
						lowres_filename = "LOWRES"+self.getMediaInfo("folder")+"-"+self.getMediaInfo("file")
				else:
					print("not supported")
				print("filename: " + lowres_filename) 
				print(lowres_url)
				if custom_filename == "":
					try:
						urllib.request.urlretrieve(lowres_url, lowres_filename)
					except (HTTPError, URLError) as error:
						print("ERROR: " + str(error))
				else:
					try:
						urllib.request.urlretrieve(lowres_url, custom_filename)
					except (HTTPError, URLError) as error:
						print("ERROR: " + str(error))
			else:
				lowres_url=""
				lowres_filename=""
				if path.endswith("MP4"):
					lowres_url=path.replace('MP4', 'LRV')
					if "GH" in lowres_url:
						lowres_url=lowres_url.replace("GH","GL")
					lowres_filename="LOWRES"+path.replace('MP4', 'LRV').replace('http://' + self.ip_addr + ':8080/videos/DCIM/','').replace('/','-')
				else:
					print("not supported")
				print("filename: " + lowres_filename) 
				print(lowres_url)
				if custom_filename == "":
					try:
						urllib.request.urlretrieve(lowres_url, lowres_filename)
					except (HTTPError, URLError) as error:
						print("ERROR: " + str(error))
				else:
					try:
						urllib.request.urlretrieve(lowres_url, custom_filename)
					except (HTTPError, URLError) as error:
						print("ERROR: " + str(error))
		else:
			print("Not supported while recording or processing media.")
	##
	## Query Media Info
	##
	def getVideoInfo(self, option= "", folder = "", file= ""):
		"""Gets video information, set folder and file parameters.
		option parameters: dur/tag_count/tags/profile/w/h"""
		if option == "":
			if folder == "" and file == "":
				if self.getMediaInfo("file").endswith("MP4"):
					return urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + self.getMediaInfo("folder") + "/" + self.getMediaInfo("file") + '&t=videoinfo').read().decode('utf-8')
		else:
			data=""
			if folder == "" and file == "":
				data=urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + self.getMediaInfo("folder") + "/" + self.getMediaInfo("file") + '&t=videoinfo').read().decode('utf-8')
			if folder == "":
				if not file == "":
					if file.endswith("MP4"):
						data=urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + self.getMediaInfo("folder") + "/" + file + '&t=videoinfo').read().decode('utf-8')
			if not file == "" and not folder == "":
				data=urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + folder + "/" + file + '&t=videoinfo').read().decode('utf-8')
			jsondata=json.loads(data)
			return jsondata[option] #dur/tag_count/tags/profile/w/h
	def getPhotoInfo(self, option= "", folder= "", file = ""):
		"""Gets photo nformation, set folder and file parameters.
		option parameters: w/h/wdr/raw..."""
		if option == "":
			if folder == "" and file == "":
				if self.getMediaInfo("file").endswith("JPG"):
					return urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + self.getMediaInfo("folder") + "/" + self.getMediaInfo("file") + '&t=v4info').read().decode('utf-8')
		else:
			data=""
			if folder == "" and file == "":
				if self.getMediaInfo("file").endswith("JPG"):
					data=urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + self.getMediaInfo("folder") + "/" + self.getMediaInfo("file") + '&t=v4info').read().decode('utf-8')
			if folder == "":
				if not file == "":
					if file.endswith("JPG"):
						data=urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + self.getMediaInfo("folder") + "/" + file + '&t=v4info').read().decode('utf-8')
			if not file == "" and not folder == "" and file.endswith("JPG"):
				data=urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + folder + "/" + file + '&t=v4info').read().decode('utf-8')
			jsondata=json.loads(data)
			return jsondata[option] #"w":"4000","h":"3000" / "wdr":"0","raw":"0"
	def getPhotoEXIF(self, option="", folder="", file=""):
		"""Gets Photo EXIF data, set folder and file parameters.
		"""
		if option == "":
			if folder == "" and file == "":
				if self.getMediaInfo("file").endswith("JPG"):
					return urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + self.getMediaInfo("folder") + "/" + self.getMediaInfo("file") + '&t=exif').read().decode('utf-8')
		else:
			data=""
			if folder == "" and file == "":
				if self.getMediaInfo("file").endswith("JPG"):
					data=urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + self.getMediaInfo("folder") + "/" + self.getMediaInfo("file") + '&t=exif').read().decode('utf-8')
			if folder == "":
				if not file == "":
					if file.endswith("JPG"):
						data=urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + self.getMediaInfo("folder") + "/" + file + '&t=exif').read().decode('utf-8')
			if not file == "" and not folder == "" and file.endswith("JPG"):
				data=urllib.request.urlopen('http://' + self.ip_addr + ':8080/gp/gpMediaMetadata?p=' + folder + "/" + file + '&t=exif').read().decode('utf-8')
			jsondata=json.loads(data)
			return jsondata[option] 

	##
	## Clip functions
	##
	def getClip(self, file, resolution, frame_rate, start_ms, stop_ms):
		"""Starts a clip conversion:
		file: folder + filename
		resolution: see constants.Clip
		frame_rate: see constants.Clip
		start_ms: start of the video in ms
		stop_ms: stop of the video in ms"""
		out=""
		if "HERO4" in self.infoCamera("model_name"):
			out = self.gpControlCommand("transcode/request?source=DCIM/" + file + "&res=" + resolution + "&fps_divisor=" + frame_rate + "&in_ms=" + start_ms + "&out_ms=" + stop_ms)
		else:
			out = self.gpControlCommand("transcode/video_to_video?source=DCIM/" + file + "&res=" + resolution + "&fps_divisor=" + frame_rate + "&in_ms=" + start_ms + "&out_ms=" + stop_ms)
		video_id = json.loads(out.replace("\\","/"))
		return video_id["status"]["id"]
	def clipStatus(self, status):
		"""returns clip status"""
		resp = json.loads(self.gpControlCommand("transcode/status?id=" + status).replace("\\","/"))
		resp_parsed = resp["status"]["status"]
		return constants.Clip.TranscodeStage[resp_parsed]
	def getClipURL(self, status):
		"""gets clip URL from status"""
		resp = json.loads(self.gpControlCommand("transcode/status?id=" + status).replace("\\","/"))
		resp_parsed = resp["status"]["status"]
		if resp_parsed == 2:
			return "http://" + self.ip_addr + ":80/videos/" + resp["status"]["output"]
	def cancelClip(self, video_id):
		"""cancels clip conversion"""
		self.gpControlCommand("transcode/cancel?id=" + video_id)

	##
	## Livestreaming functions
	##
	def livestream(self,option):
		"""start livestreaming
		option = "start"/"stop"
		"""
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
	def stream(self, addr, quality=""):
		"""Starts a FFmpeg instance for streaming to an address
		addr: Address to stream to
		quality: high/medium/low
		"""
		self.livestream("start")
		if self.whichCam() == "gpcontrol":
			if "HERO4" in self.infoCamera("model_name"):
				if quality == "high":
					self.streamSettings("2400000","6")
				elif quality == "medium":
					self.streamSettings("1000000","4")
				elif quality == "low":
					self.streamSettings("250000","0")
			else:
				if quality == "high":
					self.streamSettings("4000000","7")
				elif quality == "medium":
					self.streamSettings("1000000","4")
				elif quality == "low":
					self.streamSettings("250000","0")
			subprocess.Popen("ffmpeg -f mpegts -i udp://" + self.ip_addr + ":8554 -b 800k -r 30 -f mpegts " + addr, shell=True)
			self.KeepAlive()
		elif self.whichCam() == "auth":
			subprocess.Popen("ffmpeg -i http://" + self.ip_addr + ":8080/live/amba.m3u8 -f mpegts " + addr, shell=True)
	def streamSettings(self, bitrate, resolution):
		"""Sets stream settings"""
		self.gpControlSet("62", bitrate)
		self.gpControlSet("64", resolution)
	def parse_value(self, param,value):
		if param == "video_left":
			return str(time.strftime("%H:%M:%S", time.gmtime(value)))
		if param == "rem_space":
			if value == 0:
				return "No SD"
			ammnt=1000
			if self.whichCam() == "gpcontrol" and self.infoCamera("model_name") == "HERO4 Session":
				ammnt=1
			size_bytes=value*ammnt
			size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
			i = int(math.floor(math.log(size_bytes, 1024)))
			p = math.pow(1024, i)
			size = round(size_bytes/p, 2)
			storage = "" + str(size) + str(size_name[i])
			return str(storage)
		if param == "media_size":
			size_bytes=value
			size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
			i = int(math.floor(math.log(size_bytes, 1024)))
			p = math.pow(1024, i)
			size = round(size_bytes/p, 2)
			storage = "" + str(size) + str(size_name[i])
			return str(storage)
		if self.whichCam() == "gpcontrol":
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

			if param == "video_res":		
				if value == 1:
					return "4k"
				elif value == 2:
					return "4kSV"
				elif value == 4:
					return "2k"
				elif value == 5:
					return "2kSV"
				elif value == 6:
					return "2k4by3"
				elif value == 7:
					return "1440p"
				elif value == 8:
					return "1080pSV"
				elif value == 9:
					return "1080p"
				elif value == 10:
					return "960p"
				elif value == 11:
					return "720pSV"
				elif value == 12:
					return "720p"
				elif value == 13:
					return "480p"
				elif value == 14:
					return "5.2K"
				elif value == 15:
					return "3K"
				else:
					return "out of scope"
			if param == "video_fr":
				if value == 0:
					return "240"
				elif value == 1:
					return "120"
				elif value == 2:
					return "100"
				elif value == 5:
					return "60"
				elif value == 6:
					return "50"
				elif value == 7:
					return "48"
				elif value == 8:
					return "30"
				elif value == 9:
					return "25"
				elif value == 10:
					return "24"
				else:
					return "out of scope"
		else:
			if param  == constants.Hero3Status.Mode:
				if value == "00":
					return "Video"
				if value == "01":
					return "Photo"
				if value == "02":
					return "Burst"
				if value == "03":
					return "Timelapse"
				if value == "04":
					return "Settings"
			if param == constants.Hero3Status.TimeLapseInterval:
				if value == "00":
					return "0.5s"
				if value == "01":
					return "1s"
				if value == "02":
					return "2s"
				if value == "03":
					return "5s"
				if value == "04":
					return "10s"
				if value == "05":
					return "30s"
				if value == "06":
					return "1min"
			if param == constants.Hero3Status.LED or param == constants.Hero3Status.Beep or param == constants.Hero3Status.SpotMeter or param == constants.Hero3Status.IsRecording:
				if value == "00":
					return "OFF"
				if value == "01":
					return "ON"
				if value == "02":
					return "ON"
			if param == constants.Hero3Status.FOV:
				if value == "00":
					return "Wide"
				if value == "01":
					return "Medium"
				if value == "02":
					return "Narrow"
			if param  == constants.Hero3Status.PicRes:
				if value == "5":
					return "12mp"
				if value == "6":
					return "7mp m"
				if value == "4":
					return "7mp w"
				if value == "3":
					return "5mp m"
			if param == constants.Hero3Status.VideoRes:
				if value == "00":
					return 'WVGA'
				if value == "01":
					return '720p'
				if value == "02":
					return '960p'
				if value == "03":
					return '1080p'
				if value == "04":
					return '1440p'
				if value == "05":
					return '2.7K'
				if value == "06":
					return '2.7K Cinema'
				if value == "07":
					return '4K'
				if value == "08":
					return '4K Cinema'
				if value == "09":
					return '1080p SuperView'
				if value == "0a":
					return '720p SuperView'
			if param == constants.Hero3Status.Charging:
				if value == "3":
					return "NO"
				if value == "4":
					return "YES"
			if param == constants.Hero3Status.Protune:
				if value == "4":
					return "OFF"
				if value == "6":
					return "ON"
	def overview(self):
		if self.whichCam() == "gpcontrol":
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
			print("space left in sd card: " + "" + self.parse_value("rem_space",self.getStatus(constants.Status.Status, constants.Status.STATUS.RemainingSpace)))
			print("camera SSID: " + "" + str(self.getStatus(constants.Status.Status, constants.Status.STATUS.CamName)))
			print("Is Recording: " + "" + self.parse_value("recording",self.getStatus(constants.Status.Status, constants.Status.STATUS.IsRecording)))
			print("Clients connected: " + "" + str(self.getStatus(constants.Status.Status, constants.Status.STATUS.IsConnected)))
			print("camera model: " + "" + self.infoCamera(constants.Camera.Name))
			print("firmware version: " + "" + self.infoCamera(constants.Camera.Firmware))
			print("serial number: " + "" + self.infoCamera(constants.Camera.SerialNumber))
		elif self.whichCam() == "auth":
			#HERO3
			print("camera overview")
			print("current mode: " + self.parse_value(constants.Hero3Status.Mode,self.getStatus(constants.Hero3Status.Mode)))
			print("current video resolution: " + self.parse_value(constants.Hero3Status.VideoRes,self.getStatus(constants.Hero3Status.VideoRes)))
			print("current photo resolution: " + self.parse_value(constants.Hero3Status.PicRes,self.getStatus(constants.Hero3Status.PicRes)))
			print("current timelapse interval: " + self.parse_value(constants.Hero3Status.TimeLapseInterval,self.getStatus(constants.Hero3Status.TimeLapseInterval)))
			print("current video Fov: " + self.parse_value(constants.Hero3Status.FOV,self.getStatus(constants.Hero3Status.FOV)))
			print("status lights: " + self.parse_value(constants.Hero3Status.LED,self.getStatus(constants.Hero3Status.LED)))
			print("recording: " + self.parse_value(constants.Hero3Status.IsRecording,self.getStatus(constants.Hero3Status.IsRecording)))
