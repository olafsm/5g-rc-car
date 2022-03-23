import paho.mqtt.client as mqtt #import the client1
import time
class messager:
    def __init__(self):
        self.gc = 0
        self.sc = 0
        self.gas = 0
        self.steer = 0
    def on_message(self, client, userdata, message):
        t = int(message.payload.decode("utf-8"))
        if(message.topic == "gas"):
            self.gc += 1
            self.gas += (time.time_ns() - t)/1000000
            if self.gc%10 == 0:
                print("Avg latency last 10 steer: ", self.gas/10)
                self.gc = 0

        if(message.topic == "steer"):
            self.sc += 1
            self.steer += (time.time_ns() - t)/1000000
            if self.sc%10 == 0:
                print("Avg latency last 10 steer: ", self.steer/10)
                self.sc = 0
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message2(client, userdata, message):
    t = int(message.payload.decode("utf-8"))
    t_d = (time.time_ns() - t)/1000000
    if(message.topic == "gas"):
        print("gas:", t_d)

    if(message.topic == "steer"):
        print("steer:", t_d)
def on_message(client, userdata, message):
    client.publish("ALLO", message.payload)

m = messager()

if 0:
    client = mqtt.Client("Raspi",transport="websockets")
    client.connect("smaaberg.dev", 9001)
elif 0:
    client = mqtt.Client("Raspi")
    client.connect("smaaberg.dev", 1883)
else:
    client = mqtt.Client("Raspi")
    client.connect("localhost", 1883)

client.subscribe("gas")
client.subscribe("steer")

client.on_message=on_message
client.loop_forever()


