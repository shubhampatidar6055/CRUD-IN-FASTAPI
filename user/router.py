from fastapi import APIRouter,Form,status,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from .models import *
from passlib .context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory='user/templates')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
        return pwd_context.hash(password)

@router.get('/',response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse('index.html',{'request':request})

@router.post('/create_user/')
async def create_user(request:Request,name:str = Form(...),
                      email:str = Form(...), phone:str = Form(...),
                      password:str = Form(...)):
    if await Person.exists(email=email):
        return {"status":False,"message":"Email Already Exists"}
    elif await Person.exists(phone=phone):
        return {"status":False, "message":"Phone Number Already Exists"}
    else:
        obj = await Person.create(name=name, email=email, phone=phone, Password=get_password_hash(password))
        return RedirectResponse("/",status_code=status.HTTP_302_FOUND)


@router.get('/table/',response_class=HTMLResponse)
async def table(request:Request):
    user_data = await Person.all()
    return templates.TemplateResponse('table.html',{'request':request, "user_data":user_data})
    
@router.get('/update/{id}', response_class=HTMLResponse)
async def update(request:Request, id:int):
    user_obj = await Person.get(id=id)
    return templates.TemplateResponse('update.html',{"request":request, "user_obj":user_obj})

@router.post('/update_user/')
async def update_user(request:Request, id:int=Form(...), name:str = Form(...),
                      email:str = Form(...),phone:str = Form(...)):
    user_obj = await Person.get(id=id)
    await Person.filter(id=id).update(name=name, email=email, phone=phone)
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)

@router.get('/delete/{id}', response_class=HTMLResponse)
async def delete(request:Request, id:int):
     user_obj = await Person.get(id=id).delete()
     return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)