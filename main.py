from __future__ import print_function

import os
import json
import urllib
import boto3
from utils.hcGoogleCloudApi import get_vision_api_stub #, get_vision_api
from utils.hcAwsS3Api import list_bucket, getKeyObject # , getStatsJson, setStatsJson
from utils.hcImagesApi import read_image_base64
from utils.hcMysqlApi import addRecord, getLastFeeding
from utils.hcSesApi import sendMail

def readConfigs():
	with open('config/defult.json', 'r') as f:
		config = json.load(f)

	with open(config["passwordsFile"], 'r') as f:
		passwds = json.load(f)

	config['passwords'] = passwds
	return config

def updateDb(config, key):
	from datetime import datetime
	lastModified = datetime.strptime(key.last_modified, '%a, %d %b %Y %H:%M:%S %Z')
	stats = {}
	stats['foodName'] = key.name.encode('utf-8')
	stats['updateTime'] = datetime.now()
	stats['notificationSent'] = "false"
	stats['lastModified'] = lastModified
	stats['notificationSentTimeStamp'] = datetime.min
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

# handler to deal with feeding notifications
def lambda_feeding_handler(event, context):
	config=readConfigs()
	sendMail(config)
	lastFeedingRecord = getLastFeeding(config)
	print(lastFeedingRecord)
	# if(lastFeedingRecord['notificationSent'] == 'True'):
		# return

# handler to deal with files
def lambda_handler(event, context):
	from pprint import pprint
	config=readConfigs()
	record = event['Records'][0]
	bucket = record["s3"]["bucket"]["name"]
	key = urllib.unquote_plus(record["s3"]["object"]["key"].encode("utf8"))
	keyObject = getKeyObject(config, key)
	if testImage(config, bucket, key):
		updateDb(config, keyObject)

print('Loading function')
s3 = boto3.client('s3')

# For testing locally
# varEvent = json.loads('{"Records": [{"awsRegion": "eu-central-1","eventName": "ObjectCreated:Put","eventSource": "aws:s3","eventTime": "2017-07-06T19:34:44.271Z","eventVersion": "2.0","requestParameters": {"sourceIPAddress": "159.253.248.232"},"responseElements": {"x-amz-id-2": "rlNtwjx16oYRNMEnTx4oJQMQAMWPL4mVVHGiu8K7m1wWdJfJeFK6NkQkNO769TU4DVxr5LSB8UA=","x-amz-request-id": "00F24A7F358C0C21"},"s3": {"bucket": {"arn": "arn:aws:s3:::dynamicyield","name": "dynamicyield","ownerIdentity": {"principalId": "A2G3BXRYVGPA6"}},"configurationId": "4b528f0b-447f-4aeb-bc29-994e58d616e4","object": {"eTag": "48e9fe8f275d74ac2ec08109b538b2e1","key": "123.jpg","sequencer": "00595E74B422A717BB","size": 39198},"s3SchemaVersion": "1.0"},"userIdentity": {"principalId": "A2G3BXRYVGPA6"}}]}')
# lambda_handler(varEvent, None)

lambda_feeding_handler(None, None)