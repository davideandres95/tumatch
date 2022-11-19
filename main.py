from flask import Flask, render_template, abort, url_for, json, jsonify

import json
import numpy as np
import pandas as pd
import hashlib

app = Flask(__name__, template_folder="templates")

orderbook_history = dict()
orderbook = dict()


def update_sell_order_quantity(old, new):
    # TODO fix the quantity
    # TODO fix the price
    return min(old, new)


def update_sell_order_price(old, new):
    return new


def update_buy_order_quantity(old, new):
    return old + new


def update_buy_order_price(old, new):
    return new


def update_db(requests):
    for idx in requests.index:
        # TODO improve hashing alg, concatenation can fail if cols switched
        order_str = '"{}" requested "{}" of security "{}" with action "{}"'.format(
            requests["user"][idx],
            requests["request"][idx],
            requests["security"][idx],
            requests["side"][idx],
        )
        hash_seed = "{}{}{}{}".format(
            requests["user"][idx],
            requests["request"][idx],
            requests["security"][idx],
            requests["side"][idx],
        )
        hash_object = hashlib.sha1(hash_seed.encode("utf-8"))
        hex_dig = hash_object.hexdigest()

        if orderbook_history.get(hex_dig) is None:
            print(
                "Received Order Hash: "
                + hex_dig
                + ": [  UNIQUE  ] new order registeration: %s" % order_str
            )
            orderbook_history[hex_dig] = [
                [requests["quantity"][idx]],
                [requests["price"][idx]],
            ]
        else:
            print(
                "Received Order Hash: "
                + hex_dig
                + ": [DUPLICATED] similar order found: %s" % order_str
            )
            # new order override prev price
            orderbook_history[hex_dig][0].append(requests["quantity"][idx])
            orderbook_history[hex_dig][1].append(requests["price"][idx])
            # requests.drop(requests.index[1])
            if requests["side"][idx] == "Sell":
                print(">> Updating the value of the previous Sell order..")
                requests.loc[idx, 'quantity', ] = update_sell_order_quantity(
                    orderbook_history[hex_dig][0][-1], requests["quantity"][idx]
                )
                requests.loc[idx, 'price'] = update_sell_order_price(
                    orderbook_history[hex_dig][1][-1], requests["price"][idx]
                )
            else:  # buy
                print(">> Updating the value of the previous Add order..")
                requests.loc[idx, 'quantity', ] = update_buy_order_quantity(
                    orderbook_history[hex_dig][0][-1], requests["quantity"][idx]
                )
                requests.loc[idx, 'price'] = update_buy_order_price(
                    orderbook_history[hex_dig][1][-1], requests["price"][idx]
                )
            print(
                "Order Updated to Quantity= {} and Price= {}".format(
                    orderbook_history[hex_dig][0], orderbook_history[hex_dig][1]
                )
            )
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
