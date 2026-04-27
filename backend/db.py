from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    mode = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_log(mode: str, prompt: str, response: str, latency_ms: float):
    db = SessionLocal()
    try:
        log = QueryLog(mode=mode, prompt=prompt, response=response, latency_ms=latency_ms)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    finally:
        db.close()


def get_logs(limit: int = 20):
    db = SessionLocal()
    try:
        return db.query(QueryLog).order_by(QueryLog.created_at.desc()).limit(limit).all()
    finally:
        db.close()
