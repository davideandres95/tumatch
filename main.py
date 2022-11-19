from flask import Flask, render_template, abort, url_for, json, jsonify

import json
import numpy as np
import pandas as pd
import hashlib

app = Flask(__name__, template_folder="templates")


def update_db(requests):
    for idx in requests.index:
        # TODO improve hashing alg, concatenation can fail if cols switched
        hash_seed ="{}{}{}{}".format(requests["user"][idx],requests["request"][idx],requests["security"][idx],requests["side"][idx])
        hash_object = hashlib.sha1(hash_seed.encode("utf-8"))
        hex_dig = hash_object.hexdigest()
        print(hex_dig)


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
