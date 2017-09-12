from __future__ import absolute_import
from __future__ import print_function
import boto
from boto.s3.key import Key
from datetime import datetime
import os

def store_to_s3(fname, fpath, bucket_name, delete=False, access_key=None, secret_key=None):
    start = datetime.now()
    print('Storing ' + fpath + ' to S3 as ' + fname + '...')
    if access_key and secret_key:
        conn = boto.connect_s3(access_key, secret_key)
    else:
        conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name)
    key = Key(bucket)
    key.key = fname
    key.set_contents_from_filename(fpath)
    print('Stored in ' + str(datetime.now()-start))
    
    if delete:
        print('Deleting local file.')
        os.remove(fpath)
        print('Deleted.')

def get_from_s3(fname, fpath, bucket_name, access_key=None, secret_key=None):
    start = datetime.now()
    print('Getting ' + fname + ' from S3 to ' + fpath + '...')
    if access_key and secret_key:
        conn = boto.connect_s3(access_key, secret_key)
    else:
        conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name)
    key = bucket.get_key(fname)
    key.get_contents_to_filename(fpath)
    print('Retrieved in ' + str(datetime.now()-start))


if __name__ == "__main__":
    bucket_name = 'text-datasets'
    AWS_ACCESS_KEY = 'AKIAJXGV4UGIQUIWCA4A'
    AWS_SECRET_KEY = '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'
    # fpath = os.path.expanduser('~/.keras/models/')
    # for fname in os.listdir(fpath):
    #     store_to_s3('models/' + fname, os.path.join(fpath, fname), bucket_name, delete=False, access_key=AWS_ACCESS_KEY, secret_key=AWS_SECRET_KEY)

    fname = 'HNCommentsAll.1perline.json.bz2'
    fpath = os.path.expanduser('~/HNCommentsAll.1perline.json.bz2')
    get_from_s3(fname, fpath, bucket_name, access_key=AWS_ACCESS_KEY, secret_key=AWS_SECRET_KEY)
