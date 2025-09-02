import random
import string
import json
import uuid
import time
import os

from dtc import DTC, Socket
from message_types import *

def gen_random_string(i):
    choices = string.ascii_letters + string.digits
    return "".join([choices[random.randint(0, len(choices)-1)] for j in range(i)])

def generate_data():
    # func for generate req for message
    user_index = random.randint(1, 1000)
    
    # num_user_mentions = random.randint(1, 5)
    num_user_mentions = 1
    num_urls = random.randint(1, 5)
    num_media = random.randint(1, 4)
    text = ""
    
    user_mentions = []
    for i in range(num_user_mentions):
        while True:
            user_mention_id = random.randint(1, 1000)
            if user_mention_id != user_index and user_mention_id not in user_mentions:
                user_mentions.append(user_mention_id)
                break
    
    text += " ".join(["@username_"+str(i) for i in user_mentions])
    text += " "
    
    for i in range(num_urls):
        text += ("http://"+gen_random_string(64)+" ")
    
    media_ids = []
    media_types = ["png"] * num_media
    for i in range(num_media):
        media_ids.append(gen_random_string(5))
    
    data = {
        "username": "username_" + str(user_index),
        "user_id": user_index,
        "post_type": 0,
        "text": text,
        "media_ids": ",".join(media_ids),
        "media_types": ",".join(media_types)
    }

    return json.dumps(data)

def generate_reqs(n_req):
    reqs = []
    for i in range(n_req):
        data = generate_data()
        req_id = str(uuid.uuid4())
        message = Message(type_id=MESSAGE_DATA, req_id=req_id, req=data, index=0)
        reqs.append(message)
    return reqs

def get_socket(cc_name):
    cc_ip = f"{cc_name}.openfaas-fn.svc.cluster.local"
    cc_port = 6000
    socket = Socket(f"{cc_ip}:{cc_port}")
    return socket

def get_entry(socket, func_name):
    message = Message(type_id=MESSAGE_ENTRY, req_id=None, req=func_name, index=None)
    socket.send(message)
    response = socket.recv()

    clients = []
    for func_id in response.req:
        clients.append(DTC(f"{func_id}_w", f"{func_id}_r"))

    return clients

def send_reqs(clients, st, reqs):
    for i, req in enumerate(reqs):
        client = clients[i % len(clients)]
        client.send(req)
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
    for dtc in clients:
        try:
            os.close(dtc.rf)
            os.close(dtc.wf)
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

    cc_name = "sn-cc"

    socket = get_socket(cc_name)

    entry_func = "compose-post"

    clients = get_entry(socket, entry_func)

    send_reqs(clients, st, reqs)

    res = get_res(socket)

    clear(socket)

    socket.socket.close()

    close_dtc(clients)

    return res
