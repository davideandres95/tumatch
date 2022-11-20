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
    del_requests = []
    indices_to_delete = []
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
        
        new_quantity = 0
        request_type = requests["side"][idx]
        calculated_index = idx
        if orderbook_history[request_type].get(hex_dig) is None:
            print(
                "Received Order Hash: "
                + hex_dig
                + ": [  UNIQUE  ] new order registration: %s" % order_str
            )
            new_quantity = requests["quantity"][idx]
            calculated_index = idx
            # Before validation check if the request is delete for non-existent add
            if requests["request"][calculated_index] == "Del":
                del_origin_hash_seed = "[{}]{}+{}+{}:{}".format(
                    requests["user"][idx],
                    "Add", # FIXME workaround TODO
                    requests["security"][idx],
                    requests["side"][idx],
                    requests["price"][idx]
                )
                del_origin_hex_dig = hashlib.sha1(del_origin_hash_seed.encode("utf-8")).hexdigest()
                # delete the del order always
                indices_to_delete.append(idx)
                if orderbook_history[request_type].get(del_origin_hex_dig) is None:
                    print("Delete order is requested for non-existing order. Delete Order is ignored") # TODO improve reporting
                    continue
                else:
                    del_requests.append((orderbook_history[request_type][del_origin_hex_dig][0], requests["quantity"][idx]))

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
            indices_to_delete.append(idx)
            # FIXME the index is alredy calculated why again?? calculated_index
            calculated_index =  orderbook_history[request_type].get(hex_dig)[0]
            # print("XXXX calculated_index= " + str(calculated_index))

    print(del_requests)
    # Remove from Data base the Delete requests if they exist
    # TODO store locations of delete to improve perf
    for delete_request_info  in del_requests:
        print("Found a delete of index: " + str(delete_request_info[0]))
        remaining = requests["quantity"][delete_request_info[0]] - delete_request_info[1]
        if remaining > 0:
            requests.loc[delete_request_info[0], 'quantity'] = remaining
        else:
            indices_to_delete.append(delete_request_info[0])

    return orderbook_history, requests, indices_to_delete


def match(orderbook_history, requests, indices_to_delete):
    for buy_request_hash in orderbook_history['Buy']:
        buy_index_in_requests = orderbook_history['Buy'][buy_request_hash][0]
        # TODO could be saved directly to orderbook_history
        buy_price = requests['price'][buy_index_in_requests]
        buy_quantity = requests['quantity'][buy_index_in_requests]
        remaining = buy_quantity  # TODO obsolete
        print("to buy: " + str(abs(remaining)))
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
            print("to buy remaining: " + str(abs(remaining)))
            print("to sell: " + str(sell_quantity))
            print("buying quantity: " + str(buy_quantity))
            print("selling quantity: " + str(sell_quantity))
            if remaining > 0:
                # asked buying total value is met
                indices_to_delete.append(buy_index_in_requests)
                requests.loc[sell_index_in_requests,
                             'quantity'] = remaining  # TODO recheck
                break
            else:
                # asked selling total value is met
                remaining = abs(remaining)
                requests.loc[buy_index_in_requests,
                             'quantity'] = remaining  # TODO recheck
                indices_to_delete.append(sell_index_in_requests)
                continue
    return requests, indices_to_delete


@app.route("/")
def requests_loading():
    data_element = json.loads(read_requests())
    requests = pd.json_normalize(data_element["AddOrderRequest"])
    print("Requested Orders:")
    print(requests)

    orderbook_history, requests, indices_to_delete = update_db(requests)
    requests, indices_to_delete = match(orderbook_history, requests, indices_to_delete)

    print("Final Orders:")
    requests = requests.drop(labels=indices_to_delete, axis=0)
    print(requests)

    return "</p>Requests are loaded..</p>"
