import paho.mqtt.client as paho

class CustomClient:
    def __init__(self, hostname, port, topic, client_id: str | None = ""):

        self.mqtt_client = paho.Client(client_id)
        self.hostname = hostname
        self.port = int(port)
        self.topic = topic

        self.mqtt_client.connect(self.hostname, self.port)


    def publish(self, payload):
        return self.mqtt_client.publish(self.topic, payload)