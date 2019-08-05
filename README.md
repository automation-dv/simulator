# Agent-Server Simulator

Simulator project has 3 packages:
1. agent
2. server
3. common

requirements.txt file enlists all the libraries required for the simulators to work.
Please install them using below command:
```
pip install -r requirements.txt
```

## Agent:
agent project has 2 directories:
- scripts: this directory contains all the scripts associated with agent simulation.
  - data_generator.py : Used to generate mock data/events. Data is stored in another directory (output_jsons) under agent directory.
  - message_sender.py : Used to send data to server.
  - agent.py : Mock required agents and validate results.
  
- testdata: 
  - base.json : acts as a schema to generate both valid and invalid data.
  - config.ini : file having configurable json fields, and various other configurations like agent count, event count, http url etc. required to run agent.
  
## Server:
 server project has 2 directories:
 - scripts: This directory contains all the scripts associated with agent simulation.
   - server.py : It is a flask based server which exposes apis to accept data, reset server stats, return server stats.
   - validator.py : Used to validate data/json sent by Agent against pre-defined schema.
   - server_stats.py : Used to maintain server stats such as total, accurate, inaccurate messages received.
 - schema: Consists of pre-defined json schema against which incoming data/json sent by Agent is validated.
 - logs: server logs get generated in this folder.

## Run Server
In order to run Server, please run server.py:  
```
    python server.py
```

## Run Agent
(a) Change configuration values such as agent_count, event_count, valid_data_ratio under 'config' section in config.ini as per your requirement.  
(b) Run agent.py 
```
python agent.py
```

### Agent Flow:
1. Reset stats on Server.
2. Generate valid and invalid data.
3. Simulate Agents.
4. Send data from agent to server using POST request. 
In case of only valid data, status code returned=200. 
In case of both valid + invalid data,status code returned=400
5. Fetch stats from server to validate server side accuracy.

# Sample run:
```
Server Reset successfully

*****Data Generation*****
Started
Completed

Total data generated: 50
Valid data: 35
Invalid data: 15

*****Agents Simulation*****
Total Agents Simulated: 5
	Data sent to server by Agent-4 : Status code 400
	Data sent to server by Agent-5 : Status code 400
	Data sent to server by Agent-1 : Status code 400
	Data sent to server by Agent-2 : Status code 400
	Data sent to server by Agent-3 : Status code 400
Completed

*****Fetching stats from Server*****
Total data received by Server: 50
Valid data received by Server: 35
Invalid data received by Server: 15

Result: No loss of data

Process finished with exit code 0
```
