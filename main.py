from functools import lru_cache
from typing import List

from fastapi import FastAPI, Depends
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr, BaseSettings
from starlette.responses import JSONResponse

app = FastAPI()


class Settings(BaseSettings):
    app_name: str = "Namaz Timings Pakistan"
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: str
    mail_server: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


class EmailModel(BaseModel):
    body: str
    to: EmailStr
    title: str


class PushTokenModel(BaseModel):
    tokens: List[str]


@app.get("/")
async def root():
    return {"message": "Namaz Timings Pakistan Api"}


@app.post('/email')
async def email(req_email: EmailModel, settings: Settings = Depends(get_settings)) -> JSONResponse:
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_FROM=settings.mail_from,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_server,
        MAIL_TLS=True,
        MAIL_SSL=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )
    message = MessageSchema(
        subject=req_email.title,
        recipients=[req_email.to],  # List of recipients, as many as you can pass
        body=req_email.body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@app.post('/push_notification')
async def email(req_push: PushTokenModel):
    return JSONResponse(status_code=200, content={"message": "Notification has been sent"})
