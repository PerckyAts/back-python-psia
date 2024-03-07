from flask import Flask, Response
from confluent_kafka import Consumer, KafkaError
import json

app = Flask(__name__)

conf = {
    'bootstrap.servers': 'ntx-message-queue.hive404.com:9092',
    'group.id': 'rogella',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

@app.route('/events')
def events():
    def generate():
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            else:
                message = json.loads(msg.value().decode('utf-8'))
                id = message['id']
                winner = message['winner'][0]
                accuracy = message['winner'][1]
                results = {
                    "id": id,
                    "accuracy": accuracy,
                    "result": winner
                }
                print("results:", results)
                yield 'data: {}\n\n'.format(json.dumps(message))
    return Response(generate(), content_type='text/event-stream')

if _name_ == '__main__':
    consumer.subscribe(['response'])
    print('Consumer ready..')
    app.run(debug=True, port=3001)