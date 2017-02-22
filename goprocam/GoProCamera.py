class GoPro:
	def __init__(self):
  	#nothing
		self.ip_addr = "10.5.5.9"
	
	def shutter(self, param):
		print(self.ip_addr)
		print(param)
		print("sending shutter...")