import base64
import time
import onnxruntime as ort
from rembg.session_simple import SimpleSession
from rembg import remove
from requests_toolbelt.multipart import decoder

print("initializing model...")
start = time.time_ns()/1e6
sess_opts = ort.SessionOptions()
sess_opts.inter_op_num_threads = 1
session = SimpleSession("u2net", ort.InferenceSession(
    str('/var/task/.u2net/u2net.onnx'),
    providers=ort.get_available_providers(),
    sess_options=sess_opts,
),
)
print(f"model initialized: {(time.time_ns()/1e6 - start):.1f}ms")

def handler(event, context):
    multipart_string = base64.b64decode(event['body'])

    multipart_data = decoder.MultipartDecoder(multipart_string, event["headers"]["content-type"])

    binary_content = []

    for part in multipart_data.parts:
        binary_content.append(part.content)

    output_image = remove(binary_content[0], session=session)

    return {
        "statusCode": 200,
        "body": base64.b64encode(output_image).decode('utf-8'),
        "isBase64Encoded": True,
    }