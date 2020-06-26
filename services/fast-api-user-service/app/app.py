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
def insert_user(request: Request, new_user: UserInput):
    user = User.find_by_username(username=new_user.username)
    if user:
        return JSONResponse(content={"message": "Username already exist!"}, status_code=400)

    user = User(
        username=new_user.username,
        password=bcrypt.hashpw(new_user.password.encode("UTF8"), bcrypt.gensalt()).decode("UTF8"),
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        permission=new_user.permission
    )
    user.save_to_db()

    return JSONResponse(content={"message": "Saved successfully!"}, status_code=200)


@api.put("/user")
def update_user(request: Request, new_user: UserInput):
    user = User.find_by_username(username=new_user.username)
    if not user:
        return JSONResponse(content={"message": "Username doesn't exist!"}, status_code=200)

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
    body_string = """{{"action": "user updated", "username": "{username}", "permission": "{permission}"}}""".format(
        username=user.username,
        permission=user.permission
    )
    channel.basic_publish(exchange='my_exchange', routing_key='test', body=body_string)
    connection.close()

    return JSONResponse(content={"message": "Updated successfully!"}, status_code=200)
