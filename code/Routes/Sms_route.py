from typing import List
from fastapi import APIRouter, HTTPException
from Config.Schemas import SmsBase
from sms.Sms import send_sms_via_api

sms_router = APIRouter(
    prefix="/sms",
    responses={404: {"description": "Not found"}},
)

@sms_router.post("/send_sms/")
def send_sms(sms : SmsBase):
    try:
        response = send_sms_via_api(numero=sms.numero, message=sms.message)
        return response
    except HTTPException as e:
        return e
