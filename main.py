from __future__ import print_function

import os
import json
import urllib
import boto3
from utils.hcGoogleCloudApi import get_vision_api_stub #, get_vision_api
from utils.hcAwsS3Api import list_bucket # , getStatsJson, setStatsJson
from utils.hcImagesApi import read_image_base64
from utils.hcMysqlApi import init, printRecords, addRecord, addRecordStub

def readConfigs():
    with open('config/defult.json', 'r') as f:
        config = json.load(f)

    with open(config["passwordsFile"], 'r') as f:
        passwds = json.load(f)

    config['passwords'] = passwds
    return config

def updateDb(config, key):
	from datetime import datetime
	stats = {}
	stats['foodName'] = key.name.encode('utf-8')
	stats['updateTime'] = datetime.now()
	stats['notificationSent'] = "false"
	stats['lastModified'] = key.last_modified
	stats['notificationSentTimeStamp'] = "1970-01-01T00:00:00.000Z"
	addRecord(config, stats)

def testImage(config, bucket, key):
	# response has the image content to upload to google-vision
	try:
		# response = s3.get_object(Bucket=bucket, Key=key)
		response = 0
	except Exception as e:
		print(e)
		print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
		raise e

	gVisionResponse = json.loads(get_vision_api_stub(key))
	gVisionLabels = gVisionResponse['responses'][0]['labelAnnotations']
	for label in gVisionLabels:
		print (label["description"], label["score"] , 'Searching for: ' , config['feeding']['label'], config['feeding']['minimumScore'])
		if (label['description'] != config['feeding']['label']):
			continue
		if (label['score'] * 100 < config['feeding']['minimumScore']):
			continue
		
		return True

	return False

def mainTest():
	from pprint import pprint
	config=readConfigs()
	bucketFilesList = list_bucket(config)
	for key in bucketFilesList:
		fileName = key.name.encode('utf-8')
		if not fileName.endswith(config['feeding']['imageSuffix']):
			continue
		pprint(vars(key))
		if testImage(config, config['s3']['bucket'], key):
			updateDb(config, key)

def lambda_handler(event, context):
	from pprint import pprint
	pprint(vars(event))
	pprint(vars(context))
	config=readConfigs()
	bucket = event["Records"][0]["s3"]["bucket"]["name"]
	key = urllib.unquote_plus(event["Records"][0]["s3"]["object"]["key"].encode("utf8"))
	pprint(vars(bucket))
	pprint(vars(key))
	if testImage(config, bucket, key):
		updateDb(config, key)

print('Loading function')
s3 = boto3.client('s3')
