import os
import logging
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from finalscrapper.mysecrets import access_key, secret_access_key

s3_signature ={
    'v4':'s3v4',
    'v2':'s3'
}

def create_presigned_url(bucket_name, bucket_key, expiration=3600, signature_version=s3_signature['v4']):
    
    s3_client = boto3.client('s3',
                             aws_access_key_id=access_key,
                             aws_secret_access_key=secret_access_key,
                             region_name ='ap-south-1',
                             config=Config(signature_version=signature_version)
                             )
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': bucket_key},
                                                    ExpiresIn=expiration)
        print(s3_client.list_buckets()['Owner'])
        for key in s3_client.list_objects(Bucket=bucket_name, Prefix=bucket_key)['Contents']:
            print(key['Key'])
    except ClientError as e:
        logging.error(e)
        return None
    return response
