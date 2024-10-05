# imports
import os, json
import pika # python rabbitmq library
import pika.delivery_mode
from dotenv import load_dotenv

# load environment from .env file
load_dotenv()

# rabbitmq host
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

# callback function
def update_price(ch, method, properties, body):
    # read message
    message = json.loads(body)
    print(f"Received: {message['price']} at {message['timestamp']}")
    # write to file
    with open("../BTC_PRICE.csv", "a") as f:
        f.write(f"{message['price']},{message['timestamp']}\n")
    # acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# consume messages from queue
def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue="btc-price", durable=True)
    channel.basic_consume(queue="btc-price", on_message_callback=update_price, auto_ack=False)
    channel.start_consuming()

if __name__ == "__main__":
    while True:
        consume()