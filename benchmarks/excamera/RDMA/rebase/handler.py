import subprocess
import time
import os

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    start = time.time() * 1000

    events = req
    req_id = events[0]["req_id"]

    event = {}
    for event_item in events:
        event.update(event_item)

    raw_video = "function/3.y4m"
    prev_state = f"{req_id}-2-1.state"
    interframe_ivf_fn = f"{req_id}-3-1.ivf"
    prev_initial_state = f"{req_id}-2-0.state"

    final_state = f"{req_id}-3-1.state"
    final_fn = f"{req_id}-3.ivf"

    with open(f"function/tmp/{prev_state}", 'wb') as f:
        f.write(event[prev_state])

    with open(f"function/tmp/{interframe_ivf_fn}", 'wb') as f:
        f.write(event[interframe_ivf_fn])

    with open(f"function/tmp/{prev_initial_state}", 'wb') as f:
        f.write(event[prev_initial_state])

    # rebase: Without recoding any frames, update my interframe-only ivf file's decoder states
    #./xc-enc -W -w 0.75 -i y4m -o 3.ivf -r -I 2-1.state -p 3-1.ivf -S 2-0.state -O 3-1.state 3.y4m
    ret = subprocess.run(["./function/xc-enc",
        "-W",
        "-w",
        "0.75",
        "-i",
        "y4m",
        "-o",
        f'function/tmp/{final_fn}',
        "-r",
        "-I",
        f'function/tmp/{prev_state}',
        "-p"
        f'function/tmp/{interframe_ivf_fn}',
        "-S",
        f"function/tmp/{prev_initial_state}",
        "-O",
        f'function/tmp/{final_state}',
        raw_video
        ],
        capture_output=True)

    os.remove(f"function/tmp/{prev_state}")
    os.remove(f"function/tmp/{interframe_ivf_fn}")
    os.remove(f"function/tmp/{prev_initial_state}")
    os.remove(f"function/tmp/{final_state}")
    os.remove(f"function/tmp/{final_fn}")

    response = {"req_id": req_id, "time": {}}

    for event_item in events:
        response["time"].update(event_item["time"])

    end = time.time() * 1000

    response["time"]["rebase"] = {"start": start, "end": end}

    return response
