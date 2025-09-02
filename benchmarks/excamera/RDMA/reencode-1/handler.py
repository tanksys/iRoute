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

    raw_video = f"function/{key}.y4m"

    prev_state = f"{req_id}-{int(key)-1}-0.state"
    ivf_file = f"{req_id}-{key}-0.ivf"

    interframe_ivf_fn = f"{req_id}-{key}-1.ivf"
    new_state = f"{req_id}-{key}-1.state"

    with open(f"function/tmp/{prev_state}", 'wb') as f:
        f.write(event[prev_state])

    with open(f"function/tmp/{ivf_file}", 'wb') as f:
        f.write(event[ivf_file])

    # re-encode: replace the first keyframe with an interframe
    #./xc-enc -W -w 0.75 -i y4m -o 2-1.ivf -r -I 1-0.state -p 2-0.ivf -O 2-1.state 2.y4m
    ret = subprocess.run(["./function/xc-enc",
        "-W",
        "-w",
        "0.75",
        "-i",
        "y4m",
        "-o",
        f'function/tmp/{interframe_ivf_fn}',
        "-r",
        "-I",
        f'function/tmp/{prev_state}',
        "-p"
        f'function/tmp/{ivf_file}',
        "-O",
        f'function/tmp/{new_state}',
        raw_video
        ],
        capture_output=True)
    
    response = {"req_id": req_id, "time": event["time"]}

    prev_state2 = f"{req_id}-{key}-0.state"

    response[prev_state2] = event[prev_state2]

    with open(f"function/tmp/{new_state}", "rb") as f:
        response[new_state] = f.read()

    os.remove(f"function/tmp/{prev_state}")
    os.remove(f"function/tmp/{ivf_file}")
    os.remove(f"function/tmp/{interframe_ivf_fn}")
    os.remove(f"function/tmp/{new_state}")

    end = time.time() * 1000

    response["time"]["reencode-1"] = {"start": start, "end": end}

    return response
