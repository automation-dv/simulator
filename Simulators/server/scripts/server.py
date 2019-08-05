from flask import Flask, request, abort, Response
import shutil
import os
from server_stats import ServerStats
from validator import json_validator

app = Flask(__name__)  # creating the Flask class


@app.route('/server/', methods=['POST'])
def server():
    if not request.is_json:
        abort(400)

    ServerStats.add_total(len(request.json))

    flag = True
    for event in request.json:
        print event
        event_status = True
        if not json_validator(event):
            event_status = False

        if event_status:
            ServerStats.add_accurate()
        else:
            ServerStats.add_inaccurate()
            flag = False

    if flag:
        response = Response(status=200)
    else:
        response = Response(status=400)

    return response

@app.route('/server_stats/', methods=['GET'])
def server_stats():
    return ServerStats.get_server_stats()


@app.route('/reset_stats/', methods=['GET'])
def reset_stats():
    #delete logs directory
    logs_dir = '..//logs//'
    shutil.rmtree(logs_dir)
    os.mkdir(logs_dir)

    # reset server stats
    ServerStats.reset_stats()
    return ServerStats.get_server_stats()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
