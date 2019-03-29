#!/usr/bin/env python3

import os
import boto3
from glob import glob

pem_type = 'rsa'
app_env = os.environ.get('APP_ENV')
bucket_name = f"proof{app_env}-pushpin-cert"

s3 = boto3.client('s3')

for filepath in glob("*/**"):
    print(f"File: {filepath}")
    if pem_type in filepath:
        local = filepath
        remote = os.path.basename(filepath).replace(f".{pem_type}", '')
        s3.upload_file(local, bucket_name, remote)
        print(f"Uploaded: {local}")
