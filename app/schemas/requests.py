from pydantic import BaseModel 
from typing import Optional

class RegisterIn(BaseModel):
    email: str
    password:str 

class LoginIn(RegisterIn):
    pass


class TasksIn(BaseModel):
    title:str
    description:Optional[str] = None
    status:str="Pending"


class UpdateIn(TasksIn):
    pass