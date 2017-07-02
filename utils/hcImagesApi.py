from base64 import b64encode

""" read/write utilities """

def read_image_base64(filename):
	with open(filename, 'rb') as f:
		return b64encode(f.read())
