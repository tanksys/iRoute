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

    vpxenc_fn = f"{req_id}-{key}-vpxenc.ivf"
    output_fn = f"{req_id}-{key}-0.ivf"

    ret = subprocess.run(["./function/vpxenc",
        "--ivf",
        "--codec=vp8",
        "--good",
        "--cpu-used=0",
        "--end-usage=cq",
        "--min-q=0",
        "--max-q=63",
        "--cq-level=22",
        "--buf-initial-sz=10000",
        "--buf-optimal-sz=20000",
        "--buf-sz=40000",
        "--undershoot-pct=100",
        "--passes=2",
        "--auto-alt-ref=1",
        "--threads=1",
        "--token-parts=0",
        "--tune=ssim",
        "--target-bitrate=4294967295",
        "-o",
        f"function/tmp/{vpxenc_fn}",
        raw_video],
        capture_output=True)

    ret = subprocess.run(["./function/xc-terminate-chunk",
        f"function/tmp/{vpxenc_fn}",
        f"function/tmp/{output_fn}"],
        capture_output=True)

    with open(f"function/tmp/{output_fn}", "rb") as f:
        event[output_fn] = f.read()

    os.remove(f"function/tmp/{vpxenc_fn}")
    os.remove(f"function/tmp/{output_fn}")

    end = time.time() * 1000

    event["time"] = {"vpxenc-2": {"start": start, "end": end}}

    return event
