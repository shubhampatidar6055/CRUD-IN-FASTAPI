from fastapi import APIRouter

app = APIRouter()

@app.get("/")
def get_data():
    return{"Hello World"}