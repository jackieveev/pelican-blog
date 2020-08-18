#!./venv/bin/python
from flask import Flask, request
from threading import Lock
import subprocess

app = Flask(__name__)

pre_task = None
lock = Lock()

@app.route('/webhook', methods=['POST'])
def webhook():
    print('##### receive github push message #####')
    print(request.json)
    print('\n\n')
    lock.acquire()
    global pre_task
    if pre_task is not None:
        pre_task.kill()
    pe_task = subprocess.Popen(['sh', 'build.sh'])
    lock.release()
    return 'ok'

if __name__ == '__main__':
    app.run()
