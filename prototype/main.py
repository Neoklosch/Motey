from core import Core
from flask import Flask


app = Flask(__name__)
core = Core(app)

if __name__ == '__main__':
    try:
        core.start()
    except KeyboardInterrupt as exc:
        core.stop()
