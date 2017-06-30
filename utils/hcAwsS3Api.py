import os
import boto

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

def list_bucket(config):
    from boto.s3.connection import S3Connection
    os.environ['S3_USE_SIGV4'] = 'True'
    conn = S3Connection(config['passwords']['userAccessKey'],config['passwords']['userSecretAccessKey'],host='s3.eu-central-1.amazonaws.com')
    bucket = conn.get_bucket(config['s3']['bucket'])
    return bucket.list()
