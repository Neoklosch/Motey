import requests
import datetime

example_string = '{"name": "alpine", "engine": "docker", "parameters": {"ports": ["80/tcp: 8080", "7070/udp: 9001"],' \
                 '"name": "alpine_from_motey"}, "capabilities": ["alpine", "docker", "zigbee"]}'
target_url = 'http://localhost:5000'
header_dict = {'content-type': 'application/json'}

start_time = datetime.datetime.now()

for request in range(10000):
    r = requests.post(target_url, data=example_string, headers=header_dict)

end_time = datetime.datetime.now()
delta = end_time - start_time
print(delta)
