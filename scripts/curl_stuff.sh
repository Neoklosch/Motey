#!/bin/bash

# add capability
curl -X PUT -d '[{"capability": "markus", "capability_type": "person"}]' -H "Content-Type: application/json" http://localhost:5023/v1/capabilities -v

# remove capability
curl -X DELETE -d '[{"capability": "keks", "capability_type": "blub"}]' -H "Content-Type: application/json" http://localhost:5023/v1/capabilities -v

# get all capabilities
curl -X GET http://localhost:5023/v1/capabilities -v

# get node status
curl -X GET http://localhost:5023/v1/nodestatus -v

# upload blueprint
curl -X POST -v -H "Content-Type: application/x-yaml" --data-binary @/opt/docker-stuff/tests/data/test.yaml http://localhost:5023/v1/service
curl -X POST -v -H "Content-Type: application/x-yaml" --data-binary @tests/data/test.yaml http://172.18.0.10:5023/v1/service

# get service status
curl -X GET http://localhost:5023/v1/service -v
