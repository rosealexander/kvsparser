# kvsparser

A Python module for parsing real-time [AWS Kinesis Video Streams.](https://aws.amazon.com/kinesis/video-streams/?amazon-kinesis-video-streams-resources-blog.sort-by=item.additionalFields.createdDate&amazon-kinesis-video-streams-resources-blog.sort-order=desc)

## Usage

```python
from kvsparser import Parser
...
for fragment in Parser(media):
  print(fragment.__class__, "Frames", len(fragment.images), "Tags", fragment.tags)
```

### kvsparser.Parser(media)

#### Parameters

- media - The boto3 KinesisVideoMedia [get_media response object.](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-media/client/get_media.html)

#### Returns

- **Iterator[kvsparser.Fragment]**

### kvsparser.Fragment

- **tags** (Dict) SimpleTag elements from [ebmlite.MatroskaDocument.](https://github.com/MideTechnology/ebmlite#documents)
  - AWS_KINESISVIDEO_FRAGMENT_NUMBER 
    - Number ID of the segmented video fragment.
  - AWS_KINESISVIDEO_SERVER_TIMESTAMP 
    - Server timestamp of the segmented video fragment.
  - AWS_KINESISVIDEO_PRODUCER_TIMESTAMP 
    - Producer timestamp of the segmented video fragment.
- **images** (List[numpy.ndarray]) Frames from the segmented video fragment as a ndimage.

## License

See the [LICENSE](LICENSE) file.

This library is licensed under the MIT No Attribution License and is a derivative of “
[Amazon Kinesis Video Streams Consumer Library For Python](https://github.com/aws-samples/amazon-kinesis-video-streams-consumer-library-for-python)
” by Dean Colcott, used under MIT-0.
