# imports
import os, json
import pika # python rabbitmq library
import pika.delivery_mode
from dotenv import load_dotenv
from websockets.sync.client import connect

# load environment from .env file
load_dotenv()

# rabbitmq host
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
# binance API endpoint
SOCKET_URL = "wss://fstream.binance.com/stream?streams=btcusdt@markPrice"

# global websocket connection
ws = None

# monitor BTC price from binance websockets API
def monitor():
    global ws
    if ws is None:
        ws = connect(SOCKET_URL)
    try:
        # get price and timestamp
        message = ws.recv()
        message = json.loads(message)
        price = message['data']['p']
        timestamp = message['data']['E']

        # publish message to queue
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue="btc-price", durable=True)
        channel.basic_publish(exchange="", routing_key="btc-price", body=json.dumps({"price": price, "timestamp": timestamp}), properties=pika.BasicProperties(delivery_mode=2))
        print(f"Published: {price} at {timestamp}")
        connection.close()

    except Exception as e:
        print(f"Error: {e}")
        ws = None
    

if __name__ == "__main__":
    # run forever
    while True:
        monitor()
