from typing import List

from pydantic import BaseModel


class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool
    
    class Config:
        from_attributes = True
    
    
class ListToDoResponse(BaseModel):
    todos: List[ToDoSchema]

