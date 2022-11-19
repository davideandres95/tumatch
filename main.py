from flask import Flask, render_template, abort, url_for, json, jsonify

import json
import numpy as np
import pandas as pd
import hashlib

app = Flask(__name__, template_folder="templates")

order_book = dict()


def update_db(requests):
    for idx in requests.index:
        # TODO improve hashing alg, concatenation can fail if cols switched
        hash_seed = "{}{}{}{}".format(
            requests["user"][idx],
            requests["request"][idx],
            requests["security"][idx],
            requests["side"][idx],
        )
        hash_object = hashlib.sha1(hash_seed.encode("utf-8"))
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
        if order_book.get(hex_dig) is None:
            print("Inserting the new order.. %s" % hash_seed)
            order_book[hex_dig] = [requests["quantity"][idx], requests["price"][idx]]
        else:
            print(
                "There is a similar order from same user already registered %s"
                % hash_seed
            )
            print("Updating the value of the previous order..")
            # TODO fix the quantity
            # TODO fix the price
            order_book[hex_dig] = requests["quantity"][idx]
            print("Order Updated to: %d" % order_book[hex_dig])


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

    return "</p>Requests are loaded..</p>"
