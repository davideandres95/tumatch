from flask import Flask, render_template, abort, url_for, json, jsonify

import json
import numpy as np
import pandas as pd
import hashlib

app = Flask(__name__, template_folder="templates")

# TODO generally move to object oriented
orderbook_history = {"Sell": {}, "Buy": {}}


def read_requests():
    with open("./data/client_requests.json", "r") as myfile:
        data = myfile.read()
    return data

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
            orderbook_history[request_type][hex_dig][1].append(
                requests["quantity"][idx])
            new_quantity = update_order_quantity(
                orderbook_history[request_type][hex_dig][1][0], requests["quantity"][idx]
            )
            requests.loc[orderbook_history[request_type]
                         [hex_dig][0], 'quantity'] = new_quantity
            print(
                "The previous order's quantity is updated to= {}".format(
                    new_quantity
                )
            )
            requests = requests.drop(labels=idx, axis=0)

    return orderbook_history, requests


def match(orderbook_history, requests):
    for buy_request_hash in orderbook_history['Buy']:
        buy_index_in_requests = orderbook_history['Buy'][buy_request_hash][0]
        # TODO could be saved directly to orderbook_history
        buy_price = requests['price'][buy_index_in_requests]
        buy_quantity = requests['quantity'][buy_index_in_requests]
        remaining = buy_quantity  # TODO obsolete
        # scan all sell orders
        for sell_request_hash in orderbook_history['Sell']:
            sell_index_in_requests = orderbook_history['Sell'][sell_request_hash][0]
            sell_price = requests['price'][sell_index_in_requests]
            if sell_price > buy_price:
                print("Bid Price is too low for seller to accept..")
                print("This Seller is passing the offer..")
                continue
            sell_quantity = requests['quantity'][sell_index_in_requests]

            remaining = sell_quantity - remaining
            print("to buy: " + str(remaining))
            print("to sell: " + str(sell_quantity))
            print("buying quantity: " + str(buy_quantity))
            print("selling quantity: " + str(sell_quantity))
            if remaining > 0:
                # asked buying total value is met
                requests = requests.drop(labels=buy_index_in_requests, axis=0)
                requests.loc[sell_index_in_requests,
                             'quantity'] = remaining  # TODO recheck
                break
            else:
                # asked selling total value is met
                remaining = abs(remaining)
                requests = requests.drop(labels=sell_index_in_requests, axis=0)
                continue
    return requests


@app.route("/")
def requests_loading():
    data_element = json.loads(read_requests())
    requests = pd.json_normalize(data_element["AddOrderRequest"])
    print("Requested Orders:")
    print(requests)

    orderbook_history, requests = update_db(requests)
    print("Filtered Orders:")
    print(requests)

    requests = match(orderbook_history, requests)
    print("Matched Orders:")
    print(requests)

    return "</p>Requests are loaded..</p>"
