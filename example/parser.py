import os

import boto3 as boto3

from src import Parser

KVS_STREAM_NAME = os.environ["KVS_STREAM_NAME"]

# KVS get media
session = boto3.Session()
kvs_client = session.client("kinesisvideo")
kvs_endpoint = kvs_client.get_data_endpoint(StreamName=KVS_STREAM_NAME, APIName='GET_MEDIA').get('DataEndpoint')
kvs_media_client = session.client('kinesis-video-media', endpoint_url=kvs_endpoint)
kvs_media = kvs_media_client.get_media(StreamName=KVS_STREAM_NAME, StartSelector={'StartSelectorType': 'NOW'})

# Run the Parser
try:
    print("Parsing", KVS_STREAM_NAME)
    for fragment in Parser(kvs_media):
        print(fragment.__class__, "Frames", len(fragment.images), "Tags", fragment.tags)
    print(KVS_STREAM_NAME, "complete")
except (KeyboardInterrupt, SystemExit):
    pass
