import json
import urllib.parse
import boto3
from sas7bdat import SAS7BDAT
import pandas as pd
import io

print('Loading function')

# s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


with SAS7BDAT('mwfemale_pubuse.sas7bdat') as f:
    df = f.to_data_frame()

df.to_csv('out.csv', index=False)


# s3.Bucket('cteicloud').put_object(Key='test/test.csv', Body=buffer)
# s3_client.put_object(Bucket='cteicloud', Key='test/test.csv', Body=buffer)
s3_client.upload_file('out.csv', 'cteicloud', 'test/test.csv')
