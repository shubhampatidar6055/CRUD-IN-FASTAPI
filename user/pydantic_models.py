from pydantic import BaseModel

class user(BaseModel):
    name:str
    email:str
    phone:str
    password:str

class Show(BaseModel):
    id:int

class Name(BaseModel):
    name:str