from threading import Thread
import sys, time, requests
from Queue import Queue
from data_generator import generate_data
from message_sender import do_work
from common.config_reader import ConfigReader


AGENT_COUNT = ConfigReader.readconfigfile('config', 'agent_count')
EVENT_COUNT = ConfigReader.readconfigfile('config', 'event_count')
VALID_DATA_RATIO= ConfigReader.readconfigfile('config', 'valid_data_ratio')
API_URL = ConfigReader.readconfigfile('config', 'api_url')


#Reset server
res = requests.get(ConfigReader.readconfigfile('config', 'server_stats_reset_url'))
if res.status_code == 200:
    print "Server Reset successfully"
else:
    print "Failed to Reset server"
    sys.exit(-1)

#data generation
agent_stats = generate_data(AGENT_COUNT, EVENT_COUNT, VALID_DATA_RATIO)
print "Total data generated: %d" % agent_stats['Total']
print "Valid data: %d" % agent_stats['Valid']
print "Invalid data: %d\n" % agent_stats['Invalid']

#Agents Simulation
print "*****Agents Simulation*****\nTotal Agents Simulated: %d" % AGENT_COUNT
# start = time.clock()
q = Queue(AGENT_COUNT)
for i in range(AGENT_COUNT):
    t = Thread(target=do_work, args=(q,))
    t.daemon = True
    t.start()

for i in range(1, AGENT_COUNT + 1):
        q.put("Agent-"+str(i))
q.join()
print "Completed"
# request_time = time.clock() - start
# print request_time

#Server validation
res = requests.get(ConfigReader.readconfigfile('config', 'server_stats_url'))
if res.status_code == 200:
    server_stats = res.json()
    print "\n*****Fetching stats from Server*****"
    print "Total data received by Server: %d" % server_stats['Total']
    print "Valid data received by Server: %d" % server_stats['Accurate']
    print "Invalid data received by Server: %d" % server_stats['Inaccurate']
else:
    print "\nFailed to fetch stats from server"
    sys.exit(-1)

if agent_stats['Total']==server_stats['Total'] and agent_stats['Valid']==server_stats['Accurate'] and agent_stats['Invalid']==server_stats['Inaccurate']:
    print '\nResult: No loss of data'
else:
    print '\nResult: Data lost'
