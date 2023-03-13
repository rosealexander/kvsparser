# Copyright Alexander Rose
# SPDX-License-Identifier: MIT-0.
"""
Kinesis Video Streams Parsing using AWS KinesisVideoMedia get_media response object.
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media/client/get_media.html.
"""
import io
import logging
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, AsyncIterable, Iterable

import av
import numpy
import imageio.v3 as iio
from ebmlite import loadSchema, Document

av.logging.set_level(logging.INFO)


class Mkv(Enum):
    """
    Symbolic names for select Matroska element specifications.
    https://www.matroska.org/technical/elements.html
    """
    SEGMENT = 0x18538067
    TAGS = 0x1254C367
    TAG = 0x7373
    SIMPLETAG = 0x67C8
    TAGNAME = 0x45A3
    TAGSTRING = 0x4487
    TAGBINARY = 0x4485
    CLUSTER = 0x1F43B675
    SIMPLEBLOCK = 0xA3


class Ebml(Enum):
    """
    Symbolic name for EBML Header declaration.
    https://datatracker.ietf.org/doc/html/rfc8794#section-8.1
    """
    EBML = 0x1A45DFA3


@dataclass()
class Fragment:
    """
    Dataclass container for fragment bytes and fragment dom from KinesisVideoMedia.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media/client/get_media.html
    """
    bytes: bytearray
    dom: Document

    def __str__(self):
        return str(dict(
            bytes=self.bytes.__class__,
            dom=self.dom.__class__
        ))

    @property
    def tags(self):
        return self._get_tags()

    @property
    def images(self):
        return self._get_images()

    def _get_tags(self) -> Dict:
        """
        Returns SimpleTag elements from MatroskaDocument which contain the following general information.
        AWS_KINESISVIDEO_FRAGMENT_NUMBER - Fragment number returned to the chunk.
        AWS_KINESISVIDEO_SERVER_TIMESTAMP - Server timestamp of the fragment.
        AWS_KINESISVIDEO_PRODUCER_TIMESTAMP - Producer timestamp of the fragment.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media/client/get_media.html

        :return: A dictionary of SimpleTag element names and values.
        """
        segment = next(filter(lambda c: c.id == Mkv.SEGMENT.value, self.dom))
        tag_elements = [tag_type for element in segment if element.id == Mkv.TAGS.value for tags in element if tags.id == Mkv.TAG.value for tag_type in tags if tag_type.id == Mkv.SIMPLETAG.value]
        tag_keys = [element.value for simple_tag in tag_elements for element in simple_tag if element.id == Mkv.TAGNAME.value]
        tag_values = [element.value for simple_tag in tag_elements for element in simple_tag if element.id == Mkv.TAGSTRING.value or element.id == Mkv.TAGBINARY.value]
        simple_tags = {k: v for (k, v) in zip(tag_keys, tag_values)}
        return simple_tags

    def _get_images(self) -> List[numpy.ndarray]:
        """
        Read frames from the KVS fragment bytearray as a ndimage.

        :return: A list of frames extracted from the fragment as a numpy.ndarray
        """
        return [f for f in iio.imread(io.BytesIO(self.bytes), plugin="pyav", index=...)]


class Parser:
    def __init__(self, media):
        """
        Initialize the KVS Parser.
        """
        self._media = media
        self._stream = media['Payload']
        self._schema = loadSchema('matroska.xml')
        self._buffer = bytearray()

    def __iter__(self):
        for chunk in self._stream:
            fragment = self._run(chunk)
            if fragment:
                yield fragment

    def __aiter__(self):  # pragma: no cover
        return self._run_async()

    @property
    def media(self):
        return self._media

    @media.setter
    def media(self, media):
        self._media = media
        self._stream = media['Payload']

    def _run(self, chunk):
        self._buffer.extend(chunk)

        header_elements = [element for element in self._schema.loads(self._buffer) if element.id == Ebml.EBML.value]

        if header_elements:
            offset = header_elements[0].offset
            fragment_bytes = self._buffer[: offset]
            fragment_dom = self._schema.loads(fragment_bytes)
            fragment = Fragment(bytes=fragment_bytes, dom=fragment_dom)
            self._buffer = self._buffer[offset:]
            return fragment

    async def _run_async(self) -> AsyncIterable:  # pragma: no cover
        """
        Run the asynchronous Parser.

        :return: Kinesis Video Stream Fragment.
        """
        async for chunk in self._stream:
            fragment = self._run(chunk)
            if fragment:
                yield fragment
