import json
import os
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

def testImage(config, key):
	gVisionResponse = json.loads(get_vision_api_stub(key))
	gVisionLabels = gVisionResponse['responses'][0]['labelAnnotations']
	for label in gVisionLabels:
		print label['description'], label['score'] , 'Searching for: ' , config['feeding']['label'], config['feeding']['minimumScore']
		if (label['description'] != config['feeding']['label']):
			continue
		if (label['score'] * 100 < config['feeding']['minimumScore']):
			continue
		
		return True

	return False

def main():
	from pprint import pprint
	config=readConfigs()
	bucketFilesList = list_bucket(config)
	for key in bucketFilesList:
		fileName = key.name.encode('utf-8')
		if not fileName.endswith(config['feeding']['imageSuffix']):
			continue
		pprint(vars(key))
		if testImage(config, key):
			updateDb(config, key)

main()
