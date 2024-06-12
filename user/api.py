from fastapi import APIRouter
from .models import *
from .pydantic_models import user,Show,Name,Update
from passlib .context import CryptContext



app = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
        return pwd_context.hash(password)


@app.post("/")
async def create_user(data:user):
    if await Person.exists(email=data.email):
        return {"status":False, "message":"Email Already Exists"}

    elif await Person.exists(phone=data.phone):
        return {"status":False, "message":"Phone Number Already Exists"}
    
    else:
       user_obj = await Person.create(name=data.name,email=data.email,
                                       phone=data.phone,
                                       Password=get_password_hash(data.password))
       return user_obj
    
@app.get("/show_data/")
async def show_user():
     user_obj = await Person.all()
     return user_obj

@app.post("/show_user_data/")
async def show_user_data(data:Show):
     user_obj = await Person.get(id=data.id)
     return user_obj

@app.post("/filter_data/")
async def show_user_name(data:Name):
     user_obj = await Person.filter(name=data.name)
     return user_obj

@app.delete("/delete_user/")
async def delete_user(data:Show):
     user_obj = await Person.get(id=data.id).delete()
     return user_obj

@app.put("/update_user/")
async def update_user(data:Update):
     user_obj = await Person.get(id=data.id)
     obj = await Person.filter(id=data.id).update(name=data.name,email=data.email,
                                                  phone=data.phone,)
     return obj