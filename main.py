from typing import List, Optional
from enum import IntEnum

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length = 512, description= 'Todo Name', example="Read")
    todo_description: str = Field(..., description='Description of the todo' ,example="Read 10 pages")
    priority: Priority = Field(default = Priority.LOW, description = 'Priority of the todo', example=1)

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description='Unique ID of the todo', example=1)


class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length = 512, description= 'Todo Name', example="Read")
    todo_description: Optional[str] = Field(None, description='Description of the todo' ,example="Read 10 pages")
    priority: Optional[Priority] = Field(default = None, description = 'Priority of the todo', example=1)


#Database simulation

all_todos = [
    Todo(todo_id=1, todo_name="Sports", todo_description="go to the gym.", priority=Priority.MEDIUM),
    Todo(todo_id=2, todo_name="Read", todo_description="read 10 pages.", priority=Priority.HIGH),
    Todo(todo_id=3, todo_name="Shop", todo_description="go shopping.", priority=Priority.LOW),
    Todo(todo_id=4, todo_name="Study", todo_description="study for exam.", priority=Priority.HIGH),
    Todo(todo_id=5, todo_name="Code", todo_description="work on fastapi project.", priority=Priority.MEDIUM),
]

# GET, POST, PUT, DELETE
@app.get("/")
def root():
    return {"message": "Hello, world! 🚀"}

# path parameter
@app.get("/todos/{todo_id}" , response_model=Todo, status_code=status.HTTP_200_OK)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

# query parameter /todos/?first_n=3
@app.get("/todos", response_model=List[Todo])
def get_todo(first_n: int = None):
    if first_n and first_n > 0:
        return all_todos[:first_n]
    return all_todos


# @app.post("/todos/create")
# def create_todo(todo_name: str, todo_description: str):
#     todo_id = len(all_todos) + 1
#     new_todo = {
#         "todo_id": todo_id,
#         "todo_name": todo_name,
#         "todo_description": todo_description
#     }
#     all_todos.append(new_todo)
#     return {"message": "Todo created successfully", "todo": new_todo}

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    if todo.todo_id in all_todos:
        raise HTTPException(status_code=400, detail="Todo already exists")

    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    
    new_todo = Todo(
        todo_id=new_todo_id,
        todo_name=todo.todo_name,
        todo_description=todo.todo_description,
        priority=todo.priority
    )
    
    all_todos.append(new_todo)
    return new_todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name = updated_todo.todo_name
            if updated_todo.todo_description is not None:
                todo.todo_description = updated_todo.todo_description
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo

    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail="Todo not found")











# def main():
#     print("Hello from fastapi-demo!")


# if __name__ == "__main__":
#     main()
