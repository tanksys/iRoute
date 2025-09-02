# Replace the following with your code
workflow_name = "excamera"
writer_up = ("excamera_writer", "writer_password")
reader_up = ("excamera_reader", "reader_password")

def get_lat_dist(lats, dag):
    """
    Calculate the latency distribution from the list of latencies.
    Args:
        lats: [(message_data, timestamp)]
        - message_data.req_id: str, request id
        - message_data.req: str, request result of a final stage func
        - timestamp: float, timestamp of receiving the message, in seconds

        dag: list of stages in the workflow, each stage is a list of function names

    Please replace this with your actual implementation.
    """

    valid_lats = []
    for message, recv_time in lats:
        res_j = message.req
        start_times = [res_j["time"][fn]["start"] for fn in res_j["time"]]
        valid_lats.append(recv_time * 1000 - min(start_times))

    valid_lats.sort()

    avg_lat = sum(valid_lats) / len(valid_lats) if valid_lats else 0
    p99_lat = valid_lats[int(len(valid_lats) * 0.99)] if valid_lats else 0

    return f"avg: {avg_lat:.2f} ms, p99: {p99_lat:.2f} ms, total: {len(valid_lats)} requests"
    


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    return req
