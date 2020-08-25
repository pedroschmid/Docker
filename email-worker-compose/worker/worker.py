import redis
import json
import os
from time import sleep
from random import randint

if __name__ == '__main__':
    REDIS_HOST = os.getenv('REDIS_HOST', 'queue')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    while True:
        message = json.loads(r.blop('sender')[1])