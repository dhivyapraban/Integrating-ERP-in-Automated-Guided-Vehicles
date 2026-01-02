from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    robno = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(IST)
    )  
    status = Column(String) 