import os
from fastapi import Depends, FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
import dotenv
from Login.Login import auth_router
from Config.Database import SessionLocal, init_db
from Dependencies.Dependencies import get_current_active_user
from Routes.Sms_route import sms_router
from Routes.User_route import router, router
from Routes.Producer_route import kafka_router
from Routes.PreMatchAnalisis_route import router_analyze
from Routes.Consumer_route import consume_router

from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()


app = FastAPI(
    title="Jarvis",
    version=os.getenv("APP_VERSION"),
    docs_url=str(os.getenv("SWAGGER_URL")),
)


origins = [
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response



init_db()
# Example usage:



app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(sms_router, prefix="/api", tags=["sms"])
app.include_router(kafka_router, prefix="", tags=["kafka"])

app.include_router(router, prefix="/api", tags=["users"])
app.include_router(router_analyze, prefix="/api", tags=["pre_match_analisis"])

app.include_router(consume_router, prefix="/api", tags=["kafka_consumer"])




@app.get("/")
async def root():
    return {"message": "Hello Jarvis"}



if __name__ == '__main__':
    import uvicorn
    _host=str(os.getenv("UVC_HOST"))
    uvicorn.run("main:app", host=_host, port=8000, reload=True)
