# Project_1/attendance_service/app/schemas.py
from pydantic import BaseModel
from datetime import datetime


class ClassCreate(BaseModel):
    name:str

class ClassResponse(BaseModel):
    id:str
    name:str

    model_config = {"from_attributes":True}

class AttendanceSessionCreate(BaseModel):
    duration_minutes:int


class AttendanceSessionResponse(BaseModel):
    id:str
    code:str
    expires_at:datetime

    model_config = {"from_attributes":True}


class AttendanceSubmit(BaseModel):
    code: str


class AttendanceSubmitResponse(BaseModel):
    status: str
    submitted_at: datetime

    model_config = {"from_attributes": True}
    