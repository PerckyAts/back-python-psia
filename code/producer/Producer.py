import os
from fastapi import HTTPException
import requests
import json
import base64
import dotenv
from datetime import date 

dotenv.load_dotenv()


api_url = os.getenv("KAFKA_URL")
user = os.getenv("KAFKA_USER")
pwd = os.getenv("KAFKA_PWD")

def send_kafka_via_api(id:int, 
                       first_player_name:str,
                       second_player_name:str,
                       result:str,
                       status:bool,
                       date:date,
                       accurracy:float,
                       users_id:int,
                       match_key:str,
                       ):
    try:
        url= str(api_url)
        username = str(user)
        password = str(pwd)
        
        # # Données à envoyer dans le corps de la requête
        # data = {
        #     "id": id,
        #     "message": message,
        # }
        
        # Données à envoyer pour l'analyse pré-match
        data = {
            "id": id,
            "first_player_name": first_player_name,
            "second_player_name":second_player_name,
            "result": result,
            "status": status,
            "date": date.isoformat(),
            "users_id": users_id,
            "match_key": match_key,
            "accurracy": accurracy
        }

        # En-têtes de la requête
        headers = {
            "Accept": "application/json",
            "Authorization": "Basic " + base64.b64encode((username + ":" + password).encode()).decode(),
            "Content-Type": "application/json"
        }

        # Effectuer la requête POST
        response = requests.post(url, json=data, headers=headers)
    
    
        # Afficher la réponse
        return response.text
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))

    
# import os
# from fastapi import HTTPException
# import requests
# import json
# import base64
# import dotenv

# dotenv.load_dotenv()


# api_url = os.getenv("KAFKA_URL")
# user = os.getenv("KAFKA_USER")
# pwd = os.getenv("KAFKA_PWD")

# def send_kafka_via_api(player1:str, player2:str, id:str):
#     try:
#         url= str(api_url)
#         username = str(user)
#         password = str(pwd)
        
#         # Données à envoyer dans le corps de la requête
#         data = {
#             "player1": player1,
#             "player2": player2,
#             "id": id
#         }

#         # En-têtes de la requête
#         headers = {
#             "Accept": "application/json",
#             "Authorization": "Basic " + base64.b64encode((username + ":" + password).encode()).decode(),
#             "Content-Type": "application/json"
#         }

#         # Effectuer la requête POST
#         response = requests.post(url, data=json.dumps(data), headers=headers)
    
    
#         # Afficher la réponse
#         return response.text
    
#     except:
#         raise HTTPException(status_code=503, detail="Failed to send KAFKA")