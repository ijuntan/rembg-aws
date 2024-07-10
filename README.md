# Deploying Rembg library on AWS Lambda using Docker
## This github is just a reminder for me on how to upload large packages to AWS lambda using docker.
Big thanks to peterheb https://github.com/peterheb/rembg-lambda

## Dockerfile
```
FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

RUN mkdir .u2net && curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o .u2net/u2net.onnx

COPY app.py ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]
```

Remember to first download the model because lambda function uses read-only permission for all paths except /tmp.

## Handler to receive file from api request
```python
import base64
import time
import onnxruntime as ort
from rembg.session_simple import SimpleSession
from rembg import remove
from requests_toolbelt.multipart import decoder

# Initialize Model
sess_opts = ort.SessionOptions()
sess_opts.inter_op_num_threads = 1
session = SimpleSession("u2net", ort.InferenceSession(
    str('/var/task/.u2net/u2net.onnx'),
    providers=ort.get_available_providers(),
    sess_options=sess_opts,
))

def handler(event, context):
    # decode the image received
    multipart_string = base64.b64decode(event['body'])

    # split the multipart-form
    multipart_data = decoder.MultipartDecoder(multipart_string, event["headers"]["content-type"])

    binary_content = []

    for part in multipart_data.parts:
        binary_content.append(part.content)

    # get the first array element which is the bytes for the image
    output_image = remove(binary_content[0], session=session)

    return {
        "statusCode": 200,
        "body": base64.b64encode(output_image).decode('utf-8'),
        "isBase64Encoded": True,
    }
```
If `remove()` is used without `session` parameter, lambda function will create a read-only error.
Additionally, add env variables inside lambda called `NUMBA_DISABLE_JIT` and set the value to 1 ( to disable write capability of `numba` library ).
