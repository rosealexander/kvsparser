import os

import boto3
import pytest

from src import Parser


@pytest.fixture(autouse=True, scope="session")
def get_media():
    session = boto3.Session()

    kvs_client = session.client("kinesisvideo")

    kvs_endpoint = kvs_client.get_data_endpoint(
        StreamName=os.getenv("KVS_STREAM_NAME"),
        APIName='GET_MEDIA'
    ).get('DataEndpoint')

    kvs_media_client = session.client('kinesis-video-media', endpoint_url=kvs_endpoint)

    kvs_media = kvs_media_client.get_media(
        StreamName=os.getenv("KVS_STREAM_NAME"),
        StartSelector={'StartSelectorType': 'NOW'}
    )

    pytest.media = kvs_media


@pytest.fixture(autouse=True, scope="session")
def get_fragment(get_media):
    for fragment in Parser(pytest.media):
        pytest.fragment = fragment
        break


class TestFragment:
    def test__str_(self):
        exp = "{'bytes': <class 'bytearray'>, 'dom': <class 'ebmlite.core.MatroskaDocument'>}"
        act = str(pytest.fragment)
        assert exp == act

    def test_get_tags(self):
        exp = [
            'AWS_KINESISVIDEO_FRAGMENT_NUMBER',
            'AWS_KINESISVIDEO_SERVER_TIMESTAMP',
            'AWS_KINESISVIDEO_PRODUCER_TIMESTAMP',
            'AWS_KINESISVIDEO_MILLIS_BEHIND_NOW',
            'AWS_KINESISVIDEO_CONTINUATION_TOKEN'
       ]
        act = list(pytest.fragment.tags.keys())
        assert exp == act

    def test_get_images(self):
        act = len(pytest.fragment.images)
        assert act > 0


class TestParser:
    def test_property_media(self):
        media = {'Payload': ""}
        parser = Parser(pytest.media)
        parser.media = media
        exp = parser.media
        act = media
        assert exp == act
