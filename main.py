from fastapi import Depends, FastAPI, Request
from fastapi_cognito_security import CognitoBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
auth = CognitoBearer(
    app_client_id="1fcltdedj0o44kh3j4q26455dh",
    userpool_id="us-east-1_x6TjKca5h"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:8080",
    "http://localhost:8000",
]

templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

@app.get("/api", dependencies=[Depends(auth)])
async def root(request: Request):
    print(dict(request))
    return {"message": "Hello World"}