from fastapi import FastAPI,Depends, Request
from starlette.responses import FileResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import engine, SessionLocal
from db.models import Users,Contacts
from routers import contacts, users
from security import login
from fastapi.templating import Jinja2Templates
from security.login import getCurrentUser
from models.user import User

app = FastAPI()

app.include_router(contacts.router)
app.include_router(users.router)
app.include_router(login.router)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
       
@app.get("/loginPage")
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request":request})

@app.get("/dashboard/{user}")
async def dashboard(user: str, request: Request, currentUser: User = Depends(getCurrentUser)):
    return templates.TemplateResponse("dashboard.html", {"request":request})