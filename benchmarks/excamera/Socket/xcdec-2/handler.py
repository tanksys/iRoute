import subprocess
import time
import os

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    start = time.time() * 1000

    event = req
    req_id = event["req_id"]
    key = 2

    vpxenc_fn = f"{req_id}-{key}-0.ivf"
    output_fn = f"{req_id}-{key}-0.state"

    with open(f"function/tmp/{vpxenc_fn}", 'wb') as f:
        f.write(event[vpxenc_fn])

    ret = subprocess.run(["./function/xc-dump",
        f"function/tmp/{vpxenc_fn}",
        f"function/tmp/{output_fn}"],
        capture_output=True)
    
    response = {"req_id": req_id, "time": event["time"]}

    response[vpxenc_fn] = event[vpxenc_fn]

    with open(f"function/tmp/{output_fn}", "rb") as f:
        response[output_fn] = f.read()

    os.remove(f"function/tmp/{vpxenc_fn}")
    os.remove(f"function/tmp/{output_fn}")

    end = time.time() * 1000

    response["time"]["xcdec-2"] = {"start": start, "end": end}

    return response
