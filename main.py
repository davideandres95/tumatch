from flask import Flask, render_template, abort, url_for, json, jsonify

import json
import numpy as np
import pandas as pd
import hashlib

app = Flask(__name__, template_folder="templates")

order_book = dict()


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

        if order_book.get(hex_dig) is None:
            print(
                "Received Order Hash: "
                + hex_dig
                + ": [  UNIQUE  ] new order registeration: %s" % order_str
            )
            order_book[hex_dig] = [requests["quantity"][idx], requests["price"][idx]]
        else:
            print(
                "Received Order Hash: "
                + hex_dig
                + ": [DUPLICATED] similar order found: %s" % order_str
            )
            if requests["side"][idx] == "Sell":
                print(">> Updating the value of the previous Sell order..")
                new_quantity = update_sell_order_quantity(
                    order_book[hex_dig][0], requests["quantity"][idx]
                )
                new_price = update_sell_order_price(
                    order_book[hex_dig][1], requests["price"][idx]
                )
                order_book[hex_dig] = [new_quantity, new_price]
            else:  # buy
                print(">> Updating the value of the previous Add order..")
                new_quantity = update_buy_order_quantity(
                    order_book[hex_dig][0], requests["quantity"][idx]
                )
                new_price = update_buy_order_price(
                    order_book[hex_dig][1], requests["price"][idx]
                )
                # new order override prev price
                order_book[hex_dig] = [new_quantity, new_price]
            print(
                "Order Updated to Quantity= {} and Price= {}".format(
                    order_book[hex_dig][0], order_book[hex_dig][1]
                )
            )


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
    update_db(requests)
    # TODO match()

    return "</p>Requests are loaded..</p>"
