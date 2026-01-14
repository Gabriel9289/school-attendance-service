# Project_1/attendance_service/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas
import random
import string
from datetime import datetime, timedelta


app = FastAPI(title="Time-Bound Attendance Service")



# Create tables
models.Base.metadata.create_all(bind=engine)

def generate_attendance_code(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))



@app.get("/health")
def health_check():
    return {"status": "ok"}



@app.post("/classes",response_model=schemas.ClassResponse)
def create_class(class_data:schemas.ClassCreate,db:Session = Depends(get_db)):

    teacher_id = "teacher-123"  #temporary ,auth comes later
    new_class = models.Class(name=class_data.name,teacher_id=teacher_id)
    
    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class



@app.post("/classes/{class_id}/attendance-sessions",response_model=schemas.AttendanceSessionResponse)
def create_attendance_session(class_id: str,session_data: schemas.AttendanceSessionCreate,db: Session = Depends(get_db)):
    # duration must be positive
    if session_data.duration_minutes <= 0:
        raise HTTPException(status_code=400,detail="Duration must be greater than zero")

    code = generate_attendance_code()
    now = datetime.utcnow()
    expires_at = now + timedelta(minutes=session_data.duration_minutes)

    new_session = models.AttendanceSession(class_id=class_id,code=code,created_at=now,expires_at=expires_at,is_active=True)

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session



@app.post("/attendance/submit", response_model=schemas.AttendanceSubmitResponse)
def submit_attendance(submission: schemas.AttendanceSubmit,db: Session = Depends(get_db)):
    # TEMP: hardcoded student (auth comes later)
    student_id = "student-123"

    now = datetime.utcnow()

    # 1. Find active attendance session by code
    session = (db.query(models.AttendanceSession).filter(models.AttendanceSession.code == submission.code,models.AttendanceSession.is_active == True).first())

    if not session:
        raise HTTPException(status_code=404,detail="Invalid or inactive attendance code")

    # 2. Check expiration
    if session.expires_at < now:
        session.is_active = False
        db.commit()
        raise HTTPException(status_code=400,detail="Attendance code has expired")

    # 3. Prevent duplicate submission
    existing_record = (db.query(models.AttendanceRecord).filter(models.AttendanceRecord.attendance_session_id == session.id,models.AttendanceRecord.student_id == student_id).first())

    if existing_record:
        raise HTTPException(status_code=400,detail="Attendance already submitted")

    # 4. Record attendance
    record = models.AttendanceRecord(attendance_session_id=session.id,student_id=student_id,submitted_at=now)

    db.add(record)
    db.commit()

    return {"status": "present","submitted_at": now}
