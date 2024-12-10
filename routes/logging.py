from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import AccessLog
from schemas import GeneralResponseSchema, LogTimeRangeRequest, ResponseSchema


router = APIRouter()

@router.post("/time-range", response_model=GeneralResponseSchema)
def get_logs_by_time_range(
    time_range: LogTimeRangeRequest,
    db: Session = Depends(get_db),
):
    """
    Retrieve logs within a specified time range.
    """
    try:
        logs: List[AccessLog] = (
            db.query(AccessLog)
            .filter(AccessLog.timestamp >= time_range.start_time)
            .filter(AccessLog.timestamp <= time_range.end_time)
            .order_by(AccessLog.timestamp)
            .all()
        )
        return GeneralResponseSchema(
            success=True,
            message="Logs retrieved successfully",
            data={"logs": [log.to_dict() for log in logs]}  # Convert SQLAlchemy objects to dicts
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=ResponseSchema(
                success=False,
                message="An error occured while fetching the logs"
            ).model_dump(),
        )