# Project_1/attendance_service/app/models.py
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .database import Base


def generate_uuid():
    return str(uuid.uuid4())

   
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # this is the "teacher" or "student"

    classes = relationship("Class", back_populates="teacher")


class Class(Base):
    __tablename__ = "classes"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    teacher_id = Column(String, ForeignKey("users.id"), nullable=False)

    teacher = relationship("User", back_populates="classes")
    attendance_sessions = relationship("AttendanceSession", back_populates="class_")


class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    id = Column(String, primary_key=True, default=generate_uuid)
    class_id = Column(String, ForeignKey("classes.id"), nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    class_ = relationship("Class", back_populates="attendance_sessions")
    records = relationship("AttendanceRecord", back_populates="attendance_session")


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(String, primary_key=True, default=generate_uuid)
    attendance_session_id = Column(String, ForeignKey("attendance_sessions.id"), nullable=False)
    student_id = Column(String, ForeignKey("users.id"), nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    attendance_session = relationship("AttendanceSession", back_populates="records")
