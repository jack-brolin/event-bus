import os
import uvicorn
import pika

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.app import api
from app.rabbit import update_permission

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    os.getenv("RABBITMQ_DEFAULT_HOST"),
    5672,
    '/',
    pika.PlainCredentials(os.getenv("RABBITMQ_DEFAULT_USER"), os.getenv("RABBITMQ_DEFAULT_PASS")))
)

channel = connection.channel()

channel.basic_consume(queue="my_app", on_message_callback=update_permission, auto_ack=True)
channel.start_consuming()

if __name__ == "__main__":
    uvicorn.run(app, port=8080, log_level="info")
