from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    
    processes = relationship("Process", back_populates="client")

class Process(Base):
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    cnj = Column(String, unique=True, index=True)
    title = Column(String)
    status = Column(String)
    last_update = Column(DateTime, default=datetime.utcnow)
    next_step = Column(String)
    lawyer_name = Column(String)
    client_id = Column(Integer, ForeignKey("users.id"))

    client = relationship("User", back_populates="processes")
    timeline = relationship("TimelineEvent", back_populates="process")

class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    title = Column(String)
    description = Column(String)
    icon_type = Column(String) # 'gavel', 'file', 'check', 'clock', 'user'
    status = Column(String) # 'current', 'completed'
    process_id = Column(Integer, ForeignKey("processes.id"))

    process = relationship("Process", back_populates="timeline")
