from flask import Flask, render_template, abort, url_for, json, jsonify

import json
import numpy as np
import pandas as pd
import hashlib

app = Flask(__name__, template_folder="templates")

orderbook_history = {"Sell" : {}, "Buy" : {}}

# TODO generally move to object oriented

# add-add is cumlative buy/sell
def update_order_quantity(old, new):
    return old + new

def update_db(requests):
    for idx in requests.index:
        # TODO improve hashing alg, concatenation can fail if cols switched
        order_str = '"{}" requested "{}" of security "{}" with action "{}"'.format(
            requests["user"][idx],
            requests["request"][idx],
            requests["security"][idx],
            requests["side"][idx],
            requests["price"][idx]
        )
        hash_seed = "[{}]{}+{}+{}:{}".format(
            requests["user"][idx],
            requests["request"][idx],
            requests["security"][idx],
            requests["side"][idx],
            requests["price"][idx]
        )

        hash_object = hashlib.sha1(hash_seed.encode("utf-8"))
        hex_dig = hash_object.hexdigest()

        request_type = requests["side"][idx]
        if orderbook_history[request_type].get(hex_dig) is None:
            print(
                "Received Order Hash: "
                + hex_dig
                + ": [  UNIQUE  ] new order registration: %s" % order_str
            )
            orderbook_history[request_type][hex_dig] = [
                idx, [requests["quantity"][idx]]
            ]
        else:
            print(
                "Received Order Hash: "
                + hex_dig
                + ": [DUPLICATED] similar order found: %s" % order_str
            )
            # new order override prev price
            orderbook_history[request_type][hex_dig][1].append(requests["quantity"][idx])

            requests.loc[orderbook_history[request_type][hex_dig][0], 'quantity'] = update_order_quantity(
                orderbook_history[request_type][hex_dig][1][0], requests["quantity"][idx]
            )
            print(
                "The previous order's quantity is updated to= {}".format(
                    orderbook_history[request_type][hex_dig][1][0]
                )
            )
            requests = requests.drop(labels=idx, axis=0)
    print(orderbook_history)
    return requests


def match(orderbook_history):
    # for sec in orderbook_history[]
    return orderbook_history


def read_requests():
    with open("./data/client_requests.json", "r") as myfile:
        data = myfile.read()
    return data


@app.route("/")
def requests_loading():
    data_element = json.loads(read_requests())
    requests = pd.json_normalize(data_element["AddOrderRequest"])
    print("Requested Orders:")
    print(requests)

    print("Filtered Orders:")
    requests = update_db(requests)
    print(requests)

    # print("Matched Orders:")
    # orderbook_history = match(orderbook_history)
    # print(orderbook_history)

    return "</p>Requests are loaded..</p>"
