import sys
from fastapi import HTTPException, status, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import date 
import typing as t
from Config.Model import User, PreMatchAnalisis
from Config.Schemas import PreMatchAnalisisCreate,PreMatchAnalisisBase

from sqlalchemy.orm.exc import NoResultFound

def get_preMatchAnalisis(db: Session, find_match_key: str, id_user:int):
    prematch_analysis = (
        db.query(PreMatchAnalisis)
        .filter(
            PreMatchAnalisis.match_key == find_match_key,
        )
        .filter(
            PreMatchAnalisis.users_id == id_user,
        )
        .first() 
    )
    if prematch_analysis is not None:
        return prematch_analysis
    else:
        error_message = {"result": "Not found"}
        return JSONResponse(content=error_message, status_code=200)


def create_preMatchAnalisis(
    db: Session,
    preMatchAnalisis: PreMatchAnalisisCreate = Form(...),
):
    db_preMatchAnalisis = PreMatchAnalisis(**preMatchAnalisis.dict())  
    db_preMatchAnalisis.date = preMatchAnalisis.date
    db.add(db_preMatchAnalisis)
    db.commit()
    db.refresh(db_preMatchAnalisis)
    return db_preMatchAnalisis


def update_preMatchAnalisis(
    db: Session,
    analysis_id: int,
    new_result: str,
    new_status: bool,
    new_accurracy: float
):
    prematch_analysis = db.query(PreMatchAnalisis).filter(PreMatchAnalisis.id == analysis_id).first()

    if prematch_analysis:
        prematch_analysis.result = new_result
        prematch_analysis.status = new_status
        prematch_analysis.accurracy = new_accurracy

        db.commit()
        db.refresh(prematch_analysis)

        return prematch_analysis
    else:
        raise HTTPException(status_code=404, detail="PreMatchAnalysis not found")