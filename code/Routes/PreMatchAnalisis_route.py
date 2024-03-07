from typing import List
from fastapi import Depends, HTTPException, APIRouter, Body, Query
from sqlalchemy.orm import Session
from datetime import date
from Config.Schemas import PreMatchAnalisisCreate
from producer.Producer import send_kafka_via_api
from Crud.PreMatchAnalisis_crud import get_preMatchAnalisis, create_preMatchAnalisis, update_preMatchAnalisis
from Config.Database import SessionLocal, engine, get_db

router_analyze = APIRouter(
    prefix="/analize",
    responses={404: {"description": "Not found"}},
)

@router_analyze.post("/create_analyze/")
async def create_prematch_analysis(
    db: Session = Depends(get_db),
    prematch_data: PreMatchAnalisisCreate = Body(...),
):
    new_analysis = create_preMatchAnalisis(db, prematch_data)
    # send_kafka_via_api(new_analysis.id, 
    #                    new_analysis.second_player_name, 
    #                    new_analysis.result, 
    #                    new_analysis.status,
    #                    new_analysis.first_player_name,
    #                    new_analysis.date,new_analysis.accurracy,
    #                    new_analysis.users_id,
    #                    new_analysis.match_key)
    return new_analysis

@router_analyze.get("/get_analyze/")
async def get_analyze(
    find_match_key: str = Query(...),
    id_user: int=Query(...),
    db: Session = Depends(get_db),
):
    prematch_analysis = get_preMatchAnalisis(db, find_match_key,id_user)
    return prematch_analysis


@router_analyze.put("/update_analyze/{analysis_id}")
async def update_analyze(
    analysis_id: int,
    new_result: str = Body(...),
    new_status: bool = Body(...),
    new_accurracy: float = Body(...),
    db: Session = Depends(get_db),
):
    updated_analysis = update_preMatchAnalisis(db, analysis_id, new_result, new_status, new_accurracy)
    return updated_analysis
