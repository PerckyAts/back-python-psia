# from typing import List
# from fastapi import APIRouter, HTTPException, Body
# from consumer.Consumer import kafka_consumer_function

# consume_router = APIRouter()

# @consume_router.get("/consume/")
# async def kafka_consumer_function():
#     # bootstrap_servers = 'ntx-message-queue.hive404.com:9092'
#     # group_id = 'response_consumer_group'
#     # topic = 'response'
    
#     kafka_consumer_function()
    
#     return {"status": "Kafka consumer started"}



from typing import List
from fastapi import APIRouter
from consumer.Consumer import kafka_consumer_function


consume_router = APIRouter()

@consume_router.get("/consume/")
async def consume_messages():
    received_messages = kafka_consumer_function()
    return received_messages
