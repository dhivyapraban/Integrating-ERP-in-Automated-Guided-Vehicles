from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from schemas import Todo as TodoSchema , TodoCreate
from sqlalchemy.orm import Session
from database import sessionLocal, Base, engine
from models import Todo
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependancy for DB session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET - Html
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <body>
            <h1>Hello, This is FastAPI</h1>
        </body>
    </html>
    """
    
# POST - Create TODO
@app.post("/todos", response_model = TodoSchema)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

#GET - All Todos
@app.get("/todos", response_model = list[TodoSchema])
def readTodos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

#GET - Single Todos
@app.get("/todos/{todo_id}", response_model = TodoSchema)
def readTodo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code = 404,
            detail = "Todo not found"
                            )
    return todo

#PUT - update todo
@app.put("/updateTodo/{todo_id}",response_model = TodoSchema)
def update_todo(todo_id: int, updated: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code = 404,
            detail = "Todo not found"
                            )
    for key,value in updated.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

#DELETE - delete todo
@app.delete("/deleteTodo/{todo_id}")
def deletetodo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code = 404, detail = "Todo not found")
    db.delete(todo)
    db.commit()
    return {"message":"Todo Deleted successfully"}