# from confluent_kafka import Consumer, KafkaException
# import json

# # Configuration du consommateur Kafka
# consumer_conf = {
#     'bootstrap.servers': 'ntx-message-queue.hive404.com:9092',
#     'group.id': 'response_consumer_group',
#     'auto.offset.reset': 'earliest'
# }

# consumer = Consumer(consumer_conf)
# consumer.subscribe(['response'])

# try:
#     while True:
#         msg = consumer.poll(1.0)
#         if msg is None:
#             continue
#         if msg.error():
#             raise KafkaException(msg.error())
        
#         # Décode le message JSON
#         decoded_message = json.loads(msg.value().decode('utf-8'))
#         print('Received message:', decoded_message)
    

# except KeyboardInterrupt:
#     pass

# finally:
#     consumer.close()


# from confluent_kafka import Consumer, KafkaException
# import json

# def kafka_consumer_function():
#     # Configuration du consommateur Kafka
#     consumer_conf = {
#         'bootstrap.servers': 'ntx-message-queue.hive404.com:9092',
#         'group.id': 'response_consumer_group',
#         'auto.offset.reset': 'earliest'
#     }

#     consumer = Consumer(consumer_conf)
#     consumer.subscribe(['response'])

#     try:
#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 continue
#             if msg.error():
#                 raise KafkaException(msg.error())
            
#             # Décode le message JSON
#             decoded_message = json.loads(msg.value().decode('utf-8'))
#             print('Received message:', decoded_message)

#     except KeyboardInterrupt:
#         pass

#     finally:
#         consumer.close()



from confluent_kafka import Consumer, KafkaException
import json

def kafka_consumer_function():
    # Configuration du consommateur Kafka
    consumer_conf = {
        'bootstrap.servers': 'ntx-message-queue.hive404.com:9092',
        'group.id': 'response_consumer_group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe(['response'])

    received_messages = []

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            
            # Décode le message JSON
            decoded_message = json.loads(msg.value().decode('utf-8'))
            print('Received message:', decoded_message)
            
            # Ajoute le message à la liste
            received_messages.append(decoded_message)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

    return received_messages






