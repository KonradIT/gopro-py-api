import time
import socket
import urllib.request
import json
import re
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
	def gpControlSet(self, param,value):
		#sends Parameter and value to gpControl/setting
		return urllib.request.urlopen('http://10.5.5.9/gp/gpControl/setting/' + param + '/' + value).read()
	def gpControlCommand(self, param):
		return urllib.request.urlopen('http://10.5.5.9/gp/gpControl/command/' + param).read()
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
	def shutter(self,param):
		if self.whichCam() == "gpcontrol":
			print(self.gpControlCommand("shutter?p=" + param))
		else:
			if len(param) < 1:
				param = "0" + param
			self.sendBacpac("SH",param)
	def mode(self, mode, submode=0):
		