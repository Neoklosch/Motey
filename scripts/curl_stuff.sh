#!/bin/bash

# add label
curl -X PUT -d '[{"label": "keks", "label_type": "blub"}]' -H "Content-Type: application/json" http://localhost:5023/capabilities -v

# remove label
curl -X DELETE -d '[{"label": "keks", "label_type": "blub"}]' -H "Content-Type: application/json" http://localhost:5023/capabilities -v

# get all labels
curl -X GET http://localhost:5023/capabilities -v

# get node status
curl -X GET http://localhost:5023/nodestatus -v

# upload blueprint
curl -X POST -v -H "Content-Type: application/x-yaml" --data-binary @/opt/docker-stuff/prototype/data/test.yaml http://localhost:5023/blueprint