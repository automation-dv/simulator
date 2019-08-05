import json
from jsonschema import validate, ValidationError, SchemaError

import threading

LOGS_DIR = '..//logs//'
sem = threading.Semaphore()


def json_validator(event_json):
    with open('..//schema//schema.json') as schema_file:
        schema_data = json.load(schema_file)

    try:
        validate(instance=event_json, schema=schema_data)
        return True
    except Exception as e:
        sem.acquire()
        fw = open(LOGS_DIR + 'server.logs', 'a+')
        fw.write('****************************************************************************************************')
        fw.write('\nInvalid json: %s ' % event_json)
        fw.write('\nIssue is in %s json data : %s\n' % (event_json['agent_id'], e))
        fw.close()
        sem.release()
    except ValidationError as e:
        print('invalid json %s: %s' % (event_json, e.message))
    except SchemaError as e:
        print('invalid json %s: %s' % (event_json, e))

