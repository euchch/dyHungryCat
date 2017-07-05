import os
import httplib2
import sys
from googleapiclient import discovery
from oauth2client import tools, file, client
import json

# limited preview only (sorry!)
API_DISCOVERY_FILE = 'gApi.json'

#this function exists as stub until I'll get the google-vision api crap working
def get_vision_api_stub(key):
    import random
    data = {}
    data['responses'] = []
    responses = {}
    responses['labelAnnotations'] = []
    labelsSize = random.randrange(20) + 1
    for x in range(0, labelsSize):
        labelAnnotations = {}
        # labelAnnotations["description"] = random.choice(['fruits', 'meal', 'juice', 'produce', 'food', 'dog', 'vertebrate', 'mammal', 'night', 'fair', 'amusement park', 'apple pie', 'bread']) 
        labelAnnotations["description"] = random.choice(['fruits']) 
        labelAnnotations["score"] = (random.random() / 2) + 0.5
        responses['labelAnnotations'].append(labelAnnotations)
    data['responses'].append(responses)
    return json.dumps(data)

""" Google Authentication Utilities """

def get_vision_api():
    credentials = get_api_credentials('https://www.googleapis.com/auth/cloud-platform')
    with open(API_DISCOVERY_FILE, 'r') as f:
        doc = f.read()
    return discovery.build_from_document(doc, credentials=credentials)

def get_api_credentials(scope, service_account=True):
    """ Build API client based on oAuth2 authentication """
    STORAGE = file.Storage('oAuth2.json') #local storage of oAuth tokens
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid: #check if new oAuth flow is needed
        if service_account: #server 2 server flow
            with open(API_DISCOVERY_FILE) as f:
                account = json.loads(f.read())
                email = account['client_email']
                key = account['private_key']
            credentials = client.SignedJwtAssertionCredentials(email, key, scope=scope)
            STORAGE.put(credentials)
        else: #normal oAuth2 flow
            import argparse
            CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
            FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS, scope=scope)
            PARSER = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, parents=[tools.argparser])
            FLAGS = PARSER.parse_args(sys.argv[1:])
            credentials = tools.run_flow(FLOW, STORAGE, FLAGS)

    return credentials
