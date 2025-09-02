import json

# Replace the following with your code
workflow_name = "social-network"
writer_up = ("sn_writer", "writer_password")
reader_up = ("sn_reader", "reader_password")

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
    lats_dict = {}
    for message, recv_time in lats:
        res_j = json.loads(message.req)

        if message.req_id not in lats_dict:
            lats_dict[message.req_id] = {}

        lats_dict[message.req_id].update(res_j["time"])

        for func_name in res_j["time"]:
            if func_name in dag[-1]:
                lats_dict[message.req_id][func_name]["recv_time"] = recv_time

    num_funcs = sum(len(stage) for stage in dag)

    valid_lats = []
    for req_id, v in lats_dict.items():
        if len(v) == num_funcs:
            start_time = min(v[func_name]["start_time"] for func_name in dag[0])
            end_time = max(v[func_name]["recv_time"] for func_name in dag[-1])
            valid_lats.append((end_time - start_time) * 1000)  # Convert to milliseconds

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
