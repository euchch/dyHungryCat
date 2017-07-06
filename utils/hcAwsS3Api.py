import os
import boto
import json

SIGV4_DETECT = [
    '.cn-',
    # In eu-central we support both host styles for S3
    '.eu-central',
    '-eu-central',
]
def detect_potential_s3sigv4(func):
    def _wrapper(self):
        if os.environ.get('S3_USE_SIGV4', False):
            return ['hmac-v4-s3']

        if boto.config.get('s3', 'use-sigv4', False):
            return ['hmac-v4-s3']

        if hasattr(self, 'host'):
            # If you're making changes here, you should also check
            # ``boto/iam/connection.py``, as several things there are also
            # endpoint-related.
            for test in SIGV4_DETECT:
                if test in self.host:
                    return ['hmac-v4-s3']

        return func(self)
    return _wrapper

def getBucket(config, bucket):
    print("getBucket")
    from boto.s3.connection import S3Connection
    os.environ['S3_USE_SIGV4'] = 'True'
    print("getBucket - before conn")
    conn = S3Connection(config['passwords']['userAccessKey'],config['passwords']['userSecretAccessKey'],host='s3-eu-central-1.amazonaws.com')
    print("getBucket - after conn")
    # Without falsifying the flag - call sometimes get stuck as a lambda function
    bucketObj = conn.get_bucket(bucket, validate=False)
    return bucketObj

def list_bucket(config):
    bucket = getBucket(config, config['s3']['bucket'])
    return bucket.list()

def getKeyObject(config, keyName):
    from pprint import pprint
    print("getKeyObject")
    bucket = getBucket(config, config['s3']['bucket'])
    print("getKeyObject - before getKeyObject")
    # Without falsifying the flag - call sometimes get stuck as a lambda function however - no information is returned, such as lastmodified date, which is crucial
    statsJsonFileObj = bucket.get_key(keyName)
    pprint(vars(statsJsonFileObj))
    return statsJsonFileObj
    
# Was an attempt to work with a file rather than DB, however proverd to be much slower and not worth it

# def getStatsJson(config):
#     from pprint import pprint
#     bucket = getBucket(config, config['s3']['statsBucket'])
#     statsJsonFileObj = bucket.get_key(config['s3']['feedingStatsKey'])
#     body = statsJsonFileObj.read()
#     return json.dumps(body)

# def setStatsJson(config, statsJson):
#     print "Uploading file ", statsJson
#     bucket = getBucket(config, config['s3']['statsBucket'])
#     # statsJsonFileObj = bucket.get_key(config['s3']['feedingStatsKey'])
#     for b in bucket:
#         with open('config/stats2.json') as f:
#             b.send_file(f)
#         # .send_file(f)
#     return 0