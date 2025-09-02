import time

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    start = time.time() * 1000

    events = req
    req_id = events[0]["req_id"]

    response = {"req_id": req_id, "time": {}}

    for event in events:
        response.update(event)

    for event in events:
        response["time"].update(event["time"])

    end = time.time() * 1000

    response["time"]["group"] = {"start": start, "end": end}

    return response
