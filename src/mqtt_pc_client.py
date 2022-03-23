from webbrowser import get
import paho.mqtt.client as mqtt
import time
import threading
from inputs import devices
from inputs import get_gamepad
from XBOX import XboxController

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def get_ms():
    return time.time_ns()/1000000

def on_message(client, userdata, message):
    t = int(message.payload.decode("utf-8"))
    print((time.time_ns() - t)/1000000)

def send_inputs():
    # inputs[0] fram/tilbake
    # inputs[1] høyre/venstre
    inputs = XboxController()

    last_gas_ms = get_ms()
    last_steer_ms = get_ms()
    last_gas = 0
    last_steer = 0
    while 1:
        time.sleep(0.001)
        steer, gas = inputs.read()
        #if (abs(last_steer-steer) > 0.3) or (get_ms()-last_steer_ms > 300):
        if (abs(last_steer-steer) > 0.0):
            #print(get_ms() - last_steer_ms)
            #print("Steer: ", steer)

            last_steer_ms = get_ms()
            last_steer = steer
            client.publish("steer", time.time_ns(), qos=0)
        
        if gas<0:
            gas = 0

        #if (abs(last_gas-gas) > 0.3) or (get_ms()-last_gas_ms > 300):
        if (abs(last_gas-gas) > 0.0):
            #print(get_ms() - last_gas_ms)
            #print("Gas: ", gas)

            last_gas_ms = get_ms()
            last_gas = gas
            client.publish("gas", time.time_ns(), qos=0)

if 0:
    client = mqtt.Client("pc",transport="websockets")
    client.connect("smaaberg.dev", 9001)
elif 0:
    client = mqtt.Client("pc")
    client.connect("smaaberg.dev", 1883)
else:
    client = mqtt.Client("pc")
    client.connect("localhost", 1883)

client.on_connect = on_connect
client.on_message = on_message

print("Connecting...")
send_times = []
send_times.append(time.time_ns()/1000000)
t = time.time_ns()
client.subscribe("ALLO")
x = threading.Thread(target=send_inputs, args=())
x.start()

client.loop_forever()

