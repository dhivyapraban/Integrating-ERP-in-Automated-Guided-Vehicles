from pydantic import BaseModel
from datetime import datetime
class TodoBase(BaseModel):
    task: str
    description: str | None = None
    status: str | None = None
    robno: str
    
    
class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    created_at: datetime
    class config:
        orm_mode = True  