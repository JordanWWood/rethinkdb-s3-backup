import os
import sys
import boto3
from raven import Client

errorClient = Client('SENTRY_SECRET')

os.chdir('/data')
os.system("rethinkdb dump")

session = boto3.session.Session()
client = session.client('s3',
                        region_name='ams3',
                        endpoint_url='https://ams3.digitaloceanspaces.com',
                        aws_access_key_id='KEY',
                        aws_secret_access_key='SECRET')
                        
for filename in os.listdir('/data/'):
    if filename.endswith(".gz"):
        try:
            client.upload_file('/data/' + filename, 'BUCKET', filename)
            os.remove('/data/' + filename)
            continue
        except:
            errorClient.captureException()
    else:
        continue
