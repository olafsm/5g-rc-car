import random
from webbrowser import get
import paho.mqtt.client as mqtt
import time
import threading
from XBOX import XboxController
from keyboard import KeyboardController


def translate_range(v, from_min,from_max, to_min, to_max):
    from_span = from_max - from_min
    to_span = to_max - to_min

    valueScaled = float(v - from_min) / float(from_span)

    return to_min + (valueScaled * to_span)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def get_ms():
    pass  # return time.time_ns()/1000000


def on_message(client, userdata, message):
    t = int(message.payload.decode("utf-8"))
    # print((time.time_ns() - t)/1000000)


def translate_steps(v):
    if v <= -0.9:
        return -1
    if v <= -0.5:
        return -0.66
    if v <= -0.1:
        return -0.33
    if v <= 0.1:
        return 0.0
    if v <= 0.5:
        return 0.33
    if v <= 0.9:
        return 0.66
    if v > 0.9:
        return 1.0
    return 0


def send_inputs():
    # inputs[0] fram/tilbake
    # inputs[1] høyre/venstre
    try:
        inputs = XboxController()
    except Exception as e:
        print("Couldnt find XBOX controller")
    last_gas_ms = get_ms()
    last_steer_ms = get_ms()
    last_gas = 0
    last_steer = 0
    while 1:
        #steer = random.uniform(-1,1)
        #gas = random.uniform(-1,1)
        steer, gas = inputs.read()
        if gas < 0:
            gas = 0

        steer = translate_steps(steer)
        steer = int(translate_range(steer, -1,1, 128,255))
        gas = translate_steps(gas)
        gas = int(translate_range(gas, 0,1, 0,127))

        if (abs(last_steer - steer) > 0.0003):
            print("Steer: ", steer)

            last_steer_ms = get_ms()
            last_steer = steer
            client.publish("steer", steer, qos=0)


        if (abs(last_steer - steer) > 0.0003):
            print("Gas: ", gas)

            last_gas_ms = get_ms()
            last_gas = gas
            client.publish("gas", gas+10, qos=0)


if 0:
    client = mqtt.Client("pc", transport="websockets")
    client.connect("smaaberg.dev", 9001)
elif 1:
    client = mqtt.Client("pc")
    client.connect("89.9.162.148", 1883)
else:
    client = mqtt.Client("pc")
    client.connect("localhost", 1883)

client.on_connect = on_connect
client.on_message = on_message

print("Connecting...")
send_times = []
# send_times.append(time.time_ns()/1000000)
# t = time.time_ns()
client.subscribe("ALLO")
x = threading.Thread(target=send_inputs, args=())
x.start()

client.loop_forever()

