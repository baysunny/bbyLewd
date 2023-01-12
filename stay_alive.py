from flask import Flask
from threading import Thread
import random
import time
import requests
import logging


app = Flask('')

@app.route('/')
def home():
    return "baysunny is now online"

def run():
  app.run(host='0.0.0.0',port=random.randint(2000,9000)) 

def ping(target, debug):
    while(True):
        r = requests.get(target)
        if(debug == True):
            print(r.status_code)
        time.sleep(random.randint(30,60))
def awake(target, debug=False):  
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True  
    t = Thread(target=run)
    r = Thread(target=ping, args=(target,debug,))
    t.start()
    r.start()