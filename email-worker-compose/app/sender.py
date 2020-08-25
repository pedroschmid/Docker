import psycopg2
import redis
import json
import os
from bottle import Bottle, request





class Sender(Bottle):
    def __init__(self):
        super().__init__()

        REDIS_HOST = os.getenv('REDIS_HOST', 'queue')
        REDIS_PORT = os.getenv('REDIS_PORT', 6379)
        DB_HOST = os.getenv('DB_HOST', 'db')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_NAME = os.getenv('DB_NAME', 'sender')

        dsn = f'dbname={DB_NAME} user={DB_USER} host={DB_HOST}'

        self.route('/', method='POST', callback=self.send)
        self.queue = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

        self.conn = psycopg2.connect(dsn)

    def register_message(self, subject, message):
        SQL = 'INSERT INTO emails (subject, message) VALUES (%s, %s)'

        cur = self.conn.cursor()
        cur.execute(SQL, (subject, message))
        self.conn.commit()
        cur.close()

        msg = {
            'subject': subject,
            'message': message
        }

        self.queue.rpush('sender', json.dumps(msg))

        print('Message saved successfully!')

    def send(self):
        subject = request.forms.get('subject')
        message = request.forms.get('message')

        self.register_message(subject, message)

        return 'Lined up message!! Subject: {} Message: {}'.format(subject, message)


if __name__ == '__main__':
    sender = Sender()

    sender.run(host='0.0.0.0', port=8080, debug=True)
