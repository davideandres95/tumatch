from flask import Flask, render_template, abort, url_for, json, jsonify

import json
import html

app = Flask(__name__, template_folder="templates")

# read file
with open("./data/client_requests.json", "r") as myfile:
    data = myfile.read()


@app.route("/")
def requests_loading():
    data_element = json.loads(data)
    print(data_element["AddOrderRequest"][0]["User"])

    return render_template(
        "requests_loading.html", title="page", jsonfile=json.dumps(data)
    )

if __name__ == '__main__':
    app.run(host='localhost', debug=True)