from flask import Flask, render_template, abort, url_for, json, jsonify

import json
import numpy as np
import pandas as pd

app = Flask(__name__, template_folder="templates")

# def update_db(requests, request):
#     requests['User'][]

@app.route("/")
def requests_loading():
    with open("./data/client_requests.json", "r") as myfile:
        data = myfile.read()

    data_element = json.loads(data)
    requests = pd.json_normalize(data_element["AddOrderRequest"])
    print(requests)
    
    # update_db(requests)

    return render_template(
        "requests_loading.html", title="page", jsonfile=json.dumps(data)
    )
