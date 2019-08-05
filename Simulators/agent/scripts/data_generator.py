import hashlib
import random
import tempfile
import os
import shutil
import time
from common.config_reader import ConfigReader

jsonFiles = []
file_name_list = ConfigReader.readconfigfile('json_fields', 'file_name')
extensions_list = ConfigReader.readconfigfile('json_fields', 'extensions')
JSON_OUTPUTDIR = '..//output_jsons//'
BASEJSON_FILEPATH = '..//testdata//base.json'


def generate_data(agent_count, event_count, valid_data_ratio):
    clear_outputdir()
    print "\n*****Data Generation*****\nStarted"
    for j in range(1, int(agent_count) + 1):
        with open(BASEJSON_FILEPATH) as fr:
            data = fr.readlines()
            random_agent_id = "Agent-" + str(j)
            # Generate json files as per number of events required

            valid_events = (event_count * valid_data_ratio)
            invalid_events = event_count - valid_events

            fw = open(JSON_OUTPUTDIR + random_agent_id + '.json', 'a+')
            for i in range(1, int(event_count) + 1):
                random_file_name = random.randint(0, len(file_name_list) - 1)
                temp = tempfile.NamedTemporaryFile(suffix=extensions_list[random.randint(0, len(extensions_list) - 1)],
                                                   prefix=file_name_list[random_file_name])
                try:
                    temp_name = temp.name
                    if "/" not in temp_name:
                        t_array = temp_name.split('\\')
                        file_name = t_array[len(t_array) - 1]
                    else:
                        t_array = temp_name.split('/')
                        file_name = t_array[len(t_array) - 1]
                finally:
                    # Automatically clean up the file
                    temp.close()

                if i == 1:
                    fw.write("[\n")
                valid = True
                for line in data:
                    flag = False
                    if ":" not in line:
                        fw.write("%s" % line)
                        continue
                    json_line = line.split(':')

                    if "\"sha2\"" in json_line[0]:
                        if int(invalid_events) % 2 == 0 and invalid_events != 0:
                            line = ''
                            flag = False
                            valid = False
                        else:
                            hash_object = hashlib.sha256(file_name)
                            hex_dig = hash_object.hexdigest()
                            hex_dig = hex_dig.upper()
                            json_line[1] = '\"' + hex_dig + '\",\n'
                            flag = True
                    elif "\"md5\"" in json_line[0]:
                        if invalid_events % 3 == 0 and invalid_events != 0:
                            json_line[1] = str(random.randint(1, 5000)) + ',\n'
                            valid = False
                            flag = True
                        elif int(valid_events) % 2 == 0 and valid_events != 0:
                            hash_object = hashlib.md5(file_name)
                            hex_dig = hash_object.hexdigest()
                            hex_dig = hex_dig.upper()
                            json_line[1] = '\"' + hex_dig + '\",\n'
                            flag = True
                        else:
                            line = ''
                            flag = False
                    elif "\"agent_id\"" in json_line[0]:
                        json_line[1] = '\"' + random_agent_id + '\",\n'
                        flag = True
                    elif "\"unix_time\"" in json_line[0]:
                        if invalid_events % 13 == 0 and invalid_events != 0:
                            line = ''
                            valid = False
                            flag = False
                        else:
                            timestamp = long(time.time())
                            json_line[1] = str(timestamp) + ',\n'
                            flag = True
                    elif "\"file_name\"" in json_line[0]:
                        if invalid_events % 5 == 0 and invalid_events != 0:
                            filename = random.randint(1, 10000) * 10
                            json_line[1] = str(filename) + ',\n'
                            valid = False
                        else:
                            json_line[1] = '\"' + file_name + '\",\n'
                        flag = True
                    elif "\"file_size\"" in json_line[0]:
                        if invalid_events % 7 == 0 and invalid_events != 0:
                            json_line[1] = "true" + ',\n'
                            valid = False
                        else:
                            size_of_file = random.randint(500, 5000) * 10
                            json_line[1] = str(size_of_file) + ',\n'
                        flag = True
                    elif "\"malicious\"" in json_line[0]:
                        if valid_events:
                            if random.randint(0, 1):
                                json_line[1] = "true" + '\n'
                            else:
                                json_line[1] = "false" + '\n'
                        else:
                            json_line[1] = str(random.randint(5000, 50000)) + '\n'
                            valid = False
                        flag = True

                    if flag:
                        fw.write("%s:%s" % (json_line[0], json_line[1]))
                    else:
                        fw.write("%s" % line)

                if valid:
                    valid_events -= 1
                else:
                    invalid_events -= 1

                if i != int(event_count):
                    fw.write(",\n")
                if i == int(event_count):
                    fw.write("\n]")


            fw.close()

    print "Completed\n"

    valid_events = event_count * valid_data_ratio
    invalid_events = event_count - valid_events
    status = {"Total": (event_count * agent_count), "Valid": (valid_events * agent_count), "Invalid":  (invalid_events * agent_count)}
    return status


def clear_outputdir():
    shutil.rmtree(JSON_OUTPUTDIR)
    os.mkdir(JSON_OUTPUTDIR)
