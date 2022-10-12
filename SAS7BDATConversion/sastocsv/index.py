import json
import os
import io
from sastocsv.sas7bdat import SAS7BDAT
from datetime import datetime
import pandas as pd

import boto3

t = datetime.now()
appTime = t.strftime('%Y/%m/%d %H:%M:%S')

print(appTime + ' - #########Function SAStoCSV call #########')

s3 = boto3.resource('s3')


def sasConvert(bucket, key):
    try:
        formatted_time = t.strftime('%d-%m-%y%H%M%S')
        print('**Formatted Time: ' + formatted_time)

        if key[-9:] == '.sas7bdat':
            keySubExt = key[:-9]
            keyName = keySubExt.rsplit('/', 1)
            tmpFile = keyName[1] + '-' + formatted_time + '.sas7bdat'
            tmpOutFile = keyName[1] + '-' + formatted_time + '.csv'
            s3OutName = keyName[0] + '/' + 'output/' + keyName[1] + \
                '-' + 'convertedSAS' + '-' + formatted_time + '.csv'

            print('--keySubExt:  ' + key)
            print('--keySubExt:  ' + keySubExt)
            print('--Location:   ' + keyName[0])
            print('--File Name:  ' + keyName[1])
            print('--tmpFile:    ' + tmpFile)
            print('--tmpOutFile: ' + tmpOutFile)
            print('--s3OutName:  ' + s3OutName)

            print('**Downloading SAS7BDAT File')
            s3.meta.client.download_file(bucket, key, tmpFile)

            print('**Reading SAS7BDAT File to DataFrame')
            with SAS7BDAT(tmpFile) as f:
                df = f.to_data_frame()

            print('**Converting to CSV File')
            df.to_csv(tmpOutFile, index=False)

            print('**Uploading to S3 Bucket')
            s3.meta.client.upload_file(tmpOutFile, bucket, s3OutName,
                                       ExtraArgs={"Metadata": {""}})

            os.remove(tmpFile)
            os.remove(tmpOutFile)

            return '**Success'
        else:
            print('@@@@@ Invalid File Type @@@@@')

    except Exception as e:
        print(e)
        print('@@@@@ Error converting file to CSV @@@@@')
        raise e
