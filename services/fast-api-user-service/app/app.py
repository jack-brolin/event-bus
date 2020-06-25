import os

import inspect
import bcrypt
import pika

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

from app.models import User
from app.schema import UserInput

api = APIRouter()


@api.post("/user")
def health_check(request: Request, new_user: UserInput):
    user = User.find_by_username(username=new_user.username)
    if user:
        return {"message", "Username already exist!"}

    user = User(
        username=new_user.username,
        password=bcrypt.hashpw(new_user.password.encode("UTF8"), bcrypt.gensalt()).decode("UTF8"),
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        permission=new_user.permission
    )

    user.save_to_db()

    return {"message", "Saved successfully!"}


@api.put("/user")
def health_check(request: Request, new_user: UserInput):
    user = User.find_by_username(username=new_user.username)
    if not user:
        return {"message", "Username doesn't exist!"}

    user.first_name = new_user.first_name
    user.last_name = new_user.last_name
    user.permission = new_user.permission

    user.save_to_db()

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        os.getenv("RABBITMQ_DEFAULT_HOST"),
        5672,
        '/',
        pika.PlainCredentials(os.getenv("RABBITMQ_DEFAULT_USER"), os.getenv("RABBITMQ_DEFAULT_PASS")))
    )
    channel = connection.channel()
    channel.basic_publish(exchange='my_exchange', routing_key='test', body='{"action": "user updated"}')
    connection.close()

    return {"message", "Updated successfully!"}
