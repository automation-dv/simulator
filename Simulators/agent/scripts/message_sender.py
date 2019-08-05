import requests
import json
from common.config_reader import ConfigReader

API_URL = ConfigReader.readconfigfile('config', 'api_url')

def do_work(q):
    while True:
        agent_id = q.get()
        status = get_status(agent_id)
        display_result(agent_id, status)
        q.task_done()


def get_status(agent_id):
    # print "\n% sending data to server started" % agent_id
    try:
        json_file_path = '..//output_jsons//'+agent_id+'.json'
        with open(json_file_path) as json_file:
            data = json.load(json_file)
        headers = {'Content-type': 'application/json'}
        res = requests.post(API_URL, json=data, headers=headers)
        return res.status_code
    except:
        return "error"


def display_result(agent_id, status):
    print "\tData sent to server by %s : Status code %s" % (agent_id, str(status))
