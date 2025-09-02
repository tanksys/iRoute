import json
import uuid
import time
from concurrent.futures import ThreadPoolExecutor

from dtc import Client
from message_types import *

def generate_data():
    # func for generate req for message
    return ""

def generate_reqs(n_req):
    reqs = []
    for i in range(n_req):
        req_id = str(uuid.uuid4())
        req = {"req_id": req_id}
        message = Message(type_id=MESSAGE_DATA, req_id=req_id, req=req, index=0)
        reqs.append(message)
    return reqs

def get_socket(cc_name):
    cc_ip = f"{cc_name}.openfaas-fn.svc.cluster.local"
    cc_port = 6000
    socket = Client(cc_ip, cc_port)
    return socket

def get_entry(socket, func_name):
    message = Message(type_id=MESSAGE_ENTRY, req_id=None, req=func_name, index=None)
    socket.send(message)
    response = socket.recv()

    clients = []
    for client_index, client_ip in response.req:
        clients.append(Client(client_ip, 6000))

    return clients

def send(client, data):
    client.send(data)

def send_reqs(clients, st, reqs):
    pool = ThreadPoolExecutor(max_workers=len(clients))
    for i, req in enumerate(reqs):
        for client in clients:
            pool.submit(send, client[i % len(client)], req)
        time.sleep(st)

def get_res(socket):
    message = Message(type_id=MESSAGE_LAT_DIS, req_id=None, req=None, index=None)
    socket.send(message)
    response = socket.recv()

    return response.req

def clear(socket):
    message = Message(type_id=MESSAGE_CLEAR, req_id=None, req=None, index=None)
    socket.send(message)
    socket.recv()

def close_dtc(clients):
    for entry_clients in clients:
        for dtc in entry_clients:
            try:
                dtc.socket.close()
            except Exception as e:
                pass

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    try:
        req_j = json.loads(req)
        n_req = req_j["n"]
        st = req_j["st"]
    except Exception as e:
        n_req = 11
        st = 1

    reqs = generate_reqs(n_req)

    cc_name = "excamera-cc"

    socket = get_socket(cc_name)

    entry_funcs = ["vpxenc-1", "vpxenc-2", "vpxenc-3"]

    clients = []

    for entry_func in entry_funcs:
        clients.append(get_entry(socket, entry_func))

    send_reqs(clients, st, reqs)

    res = get_res(socket)

    clear(socket)

    socket.socket.close()

    close_dtc(clients)

    return res
