from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
auth = Cognito(
    region=os.environ["REGION"], 
    userPoolId=os.environ["USERPOOLID"],
    client_id=os.environ["APPCLIENTID"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:8080",
    "http://localhost:8000",
]

class AccessUser(BaseModel):
    sub: str
    
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/access/")
def secure_access(current_user: AccessUser = Depends(auth.claim(AccessUser))):
    # access token is valid and getting user info from access token
    return f"Hello", {current_user.sub}

get_current_user = CognitoCurrentUser(
    region=os.environ["REGION"], 
    userPoolId=os.environ["USERPOOLID"],
    client_id=os.environ["APPCLIENTID"]
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

@app.get("/user/")
def secure_user(current_user: CognitoClaims = Depends(get_current_user)):
    # ID token is valid and getting user info from ID token
    return {
        "email": current_user.email,
        "userId": current_user.username,
        "username": current_user.username,
        }

@app.get("/api", dependencies=[Depends(auth)])
async def root(request: Request):
    print(dict(request))
    return {"message": "Hello World"}