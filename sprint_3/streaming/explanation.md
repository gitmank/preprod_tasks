# Data Streaming
> streaming realtime data from a source to a sink
> using rabbitmq as message broker, websockets as data source

### websockets as data source
- support a limited number of connections with higher overhead
+ allow instant bidirectional communication by keeping TCP connections open
+ ideal for small and frequent messages

### rabbitmq as message broker
+ message broker that implements AMQP
+ prioritizes delivery over throughput

##### Test rabbitmq container
> using docker
run `docker run -p 5672:5672 -d rabbitmq` to start a rabbitmq container

##### run producer
> using websockets and pika

run `python producer.py` to start a worker that will receive and publish BTC prices to the queue

##### consume messages
> using pika and file context manager

run `python consumer.py` to start a worker that will consume messages from the queue and write them to `BTC_PRICES.csv`