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
			response = urllib.request.urlopen('http://10.5.5.9/gp/gpControl/info', timeout=5).read()
			if b"HD4" in response or b"HD3.2" in response or b"HD5" in response or b"HX" in response:
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
		if camera == "detect":
			self.power_on(mac_address)
			time.sleep(5)
			try:
				response = urllib.request.urlopen('http://10.5.5.9/gp/gpControl/info', timeout=5).read()
				if b"HD4" in response or b"HD3.2" in response or b"HD5" in response or b"HX" in response:
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
			
		else:
			if camera == "auth" or camera == "HERO3" or camera == "HERO3+" or camera == "HERO2":
				self._camera="auth"
			elif camera == "gpcontrol" or camera == "HERO4" or camera == "HERO5" or camera == "HERO+":
				self._camera="gpcontrol"
				self.prepare_gpcontrol(mac_address)
			print("Connected to " + self.ip_addr)
	
	def getPassword(self):
		PASSWORD = urllib.request.urlopen('http://10.5.5.9/bacpac/sd').read()
		password = str(PASSWORD, 'utf-8')
		password_parsed=re.sub(r'\W+', '', password)
		return password_parsed
	def gpControlSet(self, param,value):
		#sends Parameter and value to gpControl/setting
		return urllib.request.urlopen('http://10.5.5.9/gp/gpControl/setting/' + param + '/' + value).read().decode('utf-8')
	
	
	def gpControlCommand(self, param):
		return urllib.request.urlopen('http://10.5.5.9/gp/gpControl/command/' + param).read().decode('utf-8')
	
	def gpControlExecute(self, param):
		return urllib.request.urlopen('http://10.5.5.9/gp/gpControl/execute?' + param).read().decode('utf-8')
	def sendCamera(self, param,value=None):
		value_notemtpy = ""
		if value:
			value_notempty=str('&p=%' + value)
		#sends parameter and value to /camera/
		urllib.request.urlopen('http://10.5.5.9/camera/' + param + '?t=' + self.getPassword() + value_notempty).read()
	
	
	def sendBacpac(self, param,value):
		#sends parameter and value to /bacpac/
		urllib.request.urlopen('http://10.5.5.9/bacpac/' + param + '?t=' + self.getPassword() + '&p=%' + value).read()
	
	
	def whichCam(self):
		# This returns what type of camera is currently connected.
		# gpcontrol: HERO4 Black and Silver, HERO5 Black and Session, HERO Session (formally known as HERO4 Session), HERO+ LCD, HERO+.
		# auth: HERO2 with WiFi BacPac, HERO3 Black/Silver/White, HERO3+ Black and Silver.
		if self._camera != "":
			return self._camera
		else:
			self.power_on(mac_address)
			time.sleep(5)
			try:
				response = urllib.request.urlopen('http://10.5.5.9/gp/gpControl/info', timeout=5).read()
				if b"HD4" in response or b"HD3.2" in response or b"HD5" in response or b"HX" in response:
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
		req=urllib.request.urlopen("http://10.5.5.9/gp/gpControl/status")
		data = req.read()
		encoding = req.info().get_content_charset('utf-8')
		json_data = json.loads(data.decode(encoding))
		return json_data[param][value]
	
	
	def getStatusRaw(self):
		if self.whichCam() == "gpcontrol":
			return urllib.request.urlopen("http://10.5.5.9/gp/gpControl/status").read().decode('utf-8')
		elif self.whichCam() == "auth":
			return urllib.request.urlopen("http://10.5.5.9/bacpac/se?t=" + self.getPassword()).read()
		else:
			print("Error, camera not defined.")
	
	def infoCamera(self, option):
		if self.whichCam() == "gpcontrol":
			info=urllib.request.urlopen('http://10.5.5.9/gp/gpControl/info')
			data = info.read()
			encoding = info.info().get_content_charset('utf-8')
			parse_read = json.loads(data.decode(encoding))
			return parse_read["info"][option]
		elif self.whichCam() == "auth":
			if option == "model_name" or option == "firmware_version":
				info=urllib.request.urlopen('http://10.5.5.9/camera/cv')
				data = info.read()
				parsed=re.sub(r'\W+', '', str(data))
				print(parsed)
			if option == "ssid":
				info=urllib.request.urlopen('http://10.5.5.9/bacpac/cv')
				data = info.read()
				parsed=re.sub(r'\W+', '', str(data))
				print(parsed)
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
	###Media:
	def getMedia(self):
		folder = ""
		file_lo = ""
		raw_data = urllib.request.urlopen('http://10.5.5.9:8080/gp/gpMediaList').read().decode('utf-8')
		json_parse = json.loads(raw_data)
		for i in json_parse['media']:
			folder=i['d']
		for i in json_parse['media']:
			for i2 in i['fs']:
				file = i2['n']
		return raw_data
	def test(self):
		raw_data=urllib.request.urlopen('http://10.5.5.9:8080/gp/gpMediaList').read().decode('utf-8')
	def getMediaInfo(self, option):
		folder = ""
		file = ""
		size = ""
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
	def ls_send(self, path):
		subprocess.Popen("ffmpeg -i 'udp://:8554' " + path, shell=True)
