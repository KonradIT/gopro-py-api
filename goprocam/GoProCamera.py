import time
import socket
import urllib.request
import json
import re
from goprocam import constants
##################################################
# Preface:                                       #
# This API Library works with All GoPro cameras, #
# it detects which camera is connected and sends #
# the appropiate URL with values.                #
##################################################

class GoPro:
	def __init__(self):
  	#nothing
		self.ip_addr = "10.5.5.9"
		response = urllib.request.urlopen('http://10.5.5.9/gp/gpControl/info').read()
		if b"HD4" in response or b"HD3.2" in response or b"HD5" in response or b"HX" in response:
			while self.getStatus(constants.Status.Status, constants.Status.STATUS.IsConnected) == 0:
				self.getStatus(constants.Status.Status, constants.Status.STATUS.IsConnected)
		print("Connected to " + self.ip_addr)
	
	
	def gpControlSet(self, param,value):
		#sends Parameter and value to gpControl/setting
		return urllib.request.urlopen('http://10.5.5.9/gp/gpControl/setting/' + param + '/' + value).read().decode('utf-8')
	
	
	def gpControlCommand(self, param):
		return urllib.request.urlopen('http://10.5.5.9/gp/gpControl/command/' + param).read().decode('utf-8')
	
	
	def sendCamera(self, param,value):
		#sends parameter and value to /camera/
		return urllib.request.urlopen('http://10.5.5.9/camera/' + param + '?t=' + getPassword() + '&p=%' + value).read()
	
	
	def sendBacpac(self, param,value):
		#sends parameter and value to /bacpac/
		return urllib.request.urlopen('http://10.5.5.9/bacpac/' + param + '?t=' + getPassword() + '&p=%' + value).read()
	
	
	def getPassword(self):
		PASSWORD = urllib.request.urlopen('http://10.5.5.9/bacpac/sd').read()
		password = str(PASSWORD, 'utf-8')
		password_parsed=re.sub(r'\W+', '', Password)
		return password_parsed
	
	
	def whichCam(self):
		response = urllib.request.urlopen('http://10.5.5.9/gp/gpControl/info').read()
		if b"HD4" in response or b"HD3.2" in response or b"HD5" in response or b"HX" in response:
			return "gpcontrol"
		else:
			response = urllib.request.urlopen('http://10.5.5.9/camera/cv').read()
			if b"Hero3" in response:
				return "auth"
	
	
	def getStatus(self, param, value):
		req=urllib.request.urlopen("http://10.5.5.9/gp/gpControl/status")
		data = req.read()
		encoding = req.info().get_content_charset('utf-8')
		json_data = json.loads(data.decode(encoding))
		return json_data[param][value]
	
	
	def getStatusRaw(self):
		return urllib.request.urlopen("http://10.5.5.9/gp/gpControl/status").read().decode('utf-8')
	
	
	def infoCamera(self, option):
		if self.whichCam() == "gpcontrol":
			info=urllib.request.urlopen('http://10.5.5.9/gp/gpControl/info')
			data = info.read()
			encoding = info.info().get_content_charset('utf-8')
			parse_read = json.loads(data.decode(encoding))
			return parse_read["info"][option]
		else:
			if option == "model_name" or option == "firmware_version":
				info=urllib.request.urlopen('http://10.5.5.9/camera/cv')
				data = info.read()
				encoding = info.info().get_content_charset('utf-8')
				parse_read = data.decode(encoding)
				parsed=re.sub(r'\W+', '', parse_read)
				print(parsed)
			if option == "ssid":
				info=urllib.request.urlopen('http://10.5.5.9/bacpac/cv')
				data = info.read()
				parsed=re.sub(r'\W+', '', str(data))
				print(parsed)
	
	def shutter(self,param):
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("shutter?p=" + param))
		else:
			if len(param) < 1:
				param = "0" + param
			self.sendBacpac("SH",param)
	
	
	def mode(self, mode, submode="0"):
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("sub_mode?mode=" + mode + "&sub_mode=" + submode))
		else:
			if len(param) < 1:
				param = "0" + param
			self.sendBacpac("CM",param)