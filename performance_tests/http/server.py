from flask import Flask, request
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

example_container_id = "346cddf529f3a92d49d6d2b6a8ceb2154eff14709c10123ef1432029e4f2864a"

@app.route('/', methods=['POST'])
def send_blueprint():
    message = request.data
    return example_container_id

app.run(host='127.0.0.1', port=5000, debug=False)
