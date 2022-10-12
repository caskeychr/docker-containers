import json
import os
import io
from sas7bdat import SAS7BDAT
from datetime import datetime
import pandas as pd

import boto3

s3 = boto3.resource('s3')

def sasConvert(bucket, key):
    print('--Loading function')
    try:
        print('--Acquiring Current Time')
        t = datetime.now()
        formatted_time = t.strftime('%d-%m-%y%H%M%S')
        print('--Formatted Time: ' + formatted_time)

        if key[-9:] == '.sas7bdat':
            print('--Generating File Names')
            keySubExt = key[:-9]
            keyName = keySubExt.rsplit('/', 1)
            tmpFile = 'sastocsv/tmp/' + keyName[1] + '-' + formatted_time + '.sas7bdat'
            tmpOutFile = 'sastocsv/output/' + keyName[1] + '-' + formatted_time + '.csv'
            s3OutName = keyName[0] + '/' + 'output/' + keyName[1] + '-' + 'convertedSAS' + '-' + formatted_time + '.csv'

            # Print filenames
            print('*keySubExt: ' + keySubExt)
            print('*keyName: ' + keyName[0] + '   2: ' + keyName[1])
            print('*tmpFile: ' + tmpFile)
            print('*tmpOutFile: ' + tmpOutFile)
            print('*s3OutName: ' + s3OutName)

            print('--Downloading SAS7BDAT File')
            s3.meta.client.download_file(bucket, key, tmpFile)

            print('--Reading SAS7BDAT File to DataFrame')
            with SAS7BDAT(tmpFile) as f:
                df = f.to_data_frame()

            print('--Converting to CSV File')
            df.to_csv(tmpOutFile, index=False)

            print('--Uploading to S3 Bucket')
            s3.meta.client.upload_file(tmpOutFile, bucket, s3OutName)

            os.remove(tmpFile)
            os.remove(tmpOutFile)

            return(s3OutName)
        else:
            print('Invalid File Type')
            return('Invalid File Type')

    except Exception as e:
        print(e)
        print('Error converting file to CSV')
        raise e
        return(e)
