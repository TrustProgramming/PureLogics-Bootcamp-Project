from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="To-Do List API")

todos: List[dict] = []
next_id = 1

class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    completed: bool

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = {"id": next_id, "title": todo.title, "completed": False}
    todos.append(new_todo)
    next_id += 1
    return new_todo

@app.get("/todos", response_model=List[Todo])
def get_todo():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def gets_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, update: TodoUpdate):
    for todo in todos:
        if todo["id"] == todo_id:
            if update.title is not None:
                todo["title"] = update.title
            if update.completed is not None:
                todo["completed"] = update.completed
            return todo
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")