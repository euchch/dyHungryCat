import json
import os
from utils.hcGoogleCloudApi import get_vision_api
from utils.hcAwsS3Api import list_bucket
from utils.hcImagesApi import read_image_base64

def readConfigs():
    with open('config/defult.json', 'r') as f:
        config = json.load(f)

    with open(config["passwordsFile"], 'r') as f:
        passwds = json.load(f)

    config['passwords'] = passwds
    return config

def make_request(inputfile):
	""" Create a request batch (one file at a time) """
	return {
		"requests":[
			{
				"image":{
	    				"content": read_image_base64(inputfile)
	    			},
				"features": [
					{
						"type":"LABEL_DETECTION",
      						"maxResults": 10
      					}
      				]
			}
		]
	}

def testImage():
    testFile='three-strawberries.jpg'
    vision = get_vision_api()
    body = make_request(testFile)
    response = vision.annotate(body=body).execute()
    print response

def main():
    config=readConfigs()
    bucketFilesList = list_bucket(config)
    for key in bucketFilesList:
        print key.name.encode('utf-8')

main()
testImage()
