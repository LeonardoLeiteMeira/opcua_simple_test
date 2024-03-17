import json
import pika

class RabbitmqPublisher:
    def __init__(self) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = "MeuTeste"
        self.__routing_key = ""
        self.__connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )
        self.__channel = pika.BlockingConnection(self.__connection_parameters).channel()

    def __reconnect(self):
        if self.__connection is not None:
            try:
                self.__connection.close()
            except pika.exceptions.AMQPError:
                pass  # Ignore errors 
        self.__connection = pika.BlockingConnection(self.__connection_parameters)
        self.__channel = self.__connection.channel()


    def send_message(self, body: dict):
        try:
            self.__channel.basic_publish(
                exchange=self.__exchange,
                routing_key=self.__routing_key,
                body=json.dumps(body),
                properties=pika.BasicProperties(
                    delivery_mode=2  # Make message persistent
                )
            )
        except (pika.exceptions.AMQPError, pika.exceptions.StreamLostError):
            print("Connection lost, reconnecting...")
            self.__reconnect()
            self.__channel.basic_publish(
                exchange=self.__exchange,
                routing_key=self.__routing_key,
                body=json.dumps(body),
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )
