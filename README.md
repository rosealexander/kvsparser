# kvsparser

[AWS Kinesis Video Streams](https://aws.amazon.com/kinesis/video-streams/?amazon-kinesis-video-streams-resources-blog.sort-by=item.additionalFields.createdDate&amazon-kinesis-video-streams-resources-blog.sort-order=desc) 
consumer for parsing real-time video.

## Usage

```python
from kvsparser import Parser
...
for fragment in Parser(media):
  print(fragment.__class__, "Frames", len(fragment.images), "Tags", fragment.tags)```
```

### kvsparser.Parser(media)

#### Parameters

- media - The boto3 KinesisVideoMedia [get_media response object.](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media/client/get_media.html)

#### Returns

- **Iterator[kvsparser.Fragment]**

### kvsparser.Fragment

- **tags** (Dict) [SimpleTag elements](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media/client/get_media.html)
from [ebmlite.MatroskaDocument](https://github.com/MideTechnology/ebmlite#documents).
  - AWS_KINESISVIDEO_FRAGMENT_NUMBER 
    - Fragment number returned to the chunk.
  - AWS_KINESISVIDEO_SERVER_TIMESTAMP 
    - Server timestamp of the fragment.
  - AWS_KINESISVIDEO_PRODUCER_TIMESTAMP 
    - Producer timestamp of the fragment.
- **images** (List[numpy.ndarray]) Frames from fragment as a ndimage.

## License

See the [LICENSE](LICENSE) file.
This library is licensed under the MIT No Attribution License and is a derivative of “Amazon Kinesis Video Streams Consumer Library For Python” by [Amazon.com, Inc. or its affiliates,
 used under MIT-0](https://raw.githubusercontent.com/aws-samples/amazon-kinesis-video-streams-consumer-library-for-python/main/LICENSE).

## Credit

[Amazon Kinesis Video Streams Consumer Library For Python](https://github.com/aws-samples/amazon-kinesis-video-streams-consumer-library-for-python) by Dean Colcott
