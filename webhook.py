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
    if pre_task is not None:
        pre_task.kill()
    pre_task = subprocess.Popen('invoke build && mv ./output/ /usr/local/nginx/html/blog')
    lock.release()
    return 'ok'

if __name__ == '__main__':
    app.run()