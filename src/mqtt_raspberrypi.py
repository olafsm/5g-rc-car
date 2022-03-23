import paho.mqtt.client as mqtt #import the client1
import time
from smbus import SMBus

bus = SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

SLAVE_ADDRESS = 0x04


def translate_range(v, from_min,from_max, to_min, to_max):
    from_span = from_max - from_min
    to_span = to_max - to_min

    valueScaled = float(v - from_min) / float(from_span)

    return to_min + (valueScaled * to_span)


class messager:
    def __init__(self):
        self.gc = 0
        self.sc = 0
        self.gas = 0
        self.steer = 0
    def on_message(self, client, userdata, message):
        try:
            t = int(message.payload.decode("utf-8"))
        except Exception as E:
            print("not integer")

        if(message.topic == "gas"):
            self.gc += 1
            self.gas += (time.time_ns() - t)/1000000
            if self.gc%10 == 0:
                print("Avg latency last 10 steer: ", self.gas/10)
                bus.write_byte_data(SLAVE_ADDRESS, 0x80)
                self.gc = 0

        if(message.topic == "steer"):
            self.sc += 1
            self.steer += (time.time_ns() - t)/1000000
            if self.sc%10 == 0:
                print("Avg latency last 10 steer: ", self.steer/10)
                bus.write_byte_data(SLAVE_ADDRESS, 0x80)
                self.sc = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def on_message(client, userdata, message):
    try:
        t = int(message.payload.decode("utf-8"))
    except Exception as E:
        print("not integer")
        return
    #t_d = (time.time_ns() - t)/1000000
    if(message.topic == "gas"):
        bus.write_byte_data(SLAVE_ADDRESS, translate_range(t, 0,1,0,127))
        print("gas:", t_d)

    if(message.topic == "steer"):
        print("steer:", t_d)
        bus.write_byte_data(SLAVE_ADDRESS, translate_range(t, 0,1,128,255))



def on_message3(client, userdata, message):
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


