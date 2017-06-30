import json
import os
from utils.hcGoogleCloudApi import get_vision_api
from utils.hcAwsS3Api import list_bucket

def readConfigs():
    with open('config/defult.json', 'r') as f:
        config = json.load(f)

    with open(config["passwordsFile"], 'r') as f:
        passwds = json.load(f)

    config['passwords'] = passwds
    return config

def main():
    config=readConfigs()
    bucketFilesList = list_bucket(config)
    for key in bucketFilesList:
        print key.name.encode('utf-8')

main()
