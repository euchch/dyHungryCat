from base64 import b64encode

""" read/write utilities """

# not in use as google api does not play nice
def read_image_base64(filename):
	with open(filename, 'rb') as f:
		return b64encode(f.read())
