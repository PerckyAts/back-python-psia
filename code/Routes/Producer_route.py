from typing import List
from fastapi import APIRouter, HTTPException,Body
from Config.Schemas import ProduceBase
from producer.Producer import send_kafka_via_api

kafka_router = APIRouter()

@kafka_router.post("/produce/")
def send_kafka(producer : ProduceBase=Body(...)):
    try:
        response = send_kafka_via_api(id=producer.id, 
                                      first_player_name=producer.first_player_name,
                                      second_player_name=producer.second_player_name,
                                      result=producer.result,
                                      status=producer.status,
                                      date=producer.date,
                                      accurracy=producer.accurracy,
                                      users_id=producer.users_id,
                                      match_key=producer.match_key,
                                      )
        return response
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))

# from typing import List
# from fastapi import APIRouter, HTTPException
# from Config.Schemas import ProduceBase
# from producer.Producer import send_kafka_via_api

# kafka_router = APIRouter()

# @kafka_router.post("/produce/")
# def send_kafka(producer: ProduceBase):
#     try:
#         response = send_kafka_via_api(
#             player1=producer.player1, 
#             player2=producer.player2, 
#             id=producer.id
#         )
#         return response
#     except HTTPException as e:
#         return e