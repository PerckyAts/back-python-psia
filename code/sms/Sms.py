import os
from fastapi import HTTPException
import requests
import json
import base64
import dotenv

dotenv.load_dotenv()


api_url = os.getenv("SMS_URL")
user = os.getenv("SMS_USER")
pwd = os.getenv("SMS_PWD")

def send_sms_via_api(numero:str, message:str):
    try:
        url= str(api_url)
        username = str(user)
        password = str(pwd)
        
        # Données à envoyer dans le corps de la requête
        data = {
            "name": "Jarvis",
            "description": "Jarvis wta sms",
            "message": message,
            "scheduledAt": "asap",
            "commercialName": "Jarvis",
            "commercialNameAsSender": True,
            "contacts": numero
        }

        # En-têtes de la requête
        headers = {
            "Accept": "application/json",
            "Authorization": "Basic " + base64.b64encode((username + ":" + password).encode()).decode(),
            "Content-Type": "application/json"
        }

        # Effectuer la requête POST
        response = requests.post(url, data=json.dumps(data), headers=headers)
        
        # Afficher la réponse
        return response.text
    except:
        raise HTTPException(status_code=503, detail="Failed to send SMS")