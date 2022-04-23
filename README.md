# 5g-rc-car
5G-styrt bil. Eksperter i team prosjekt @NTNU

# Setup & install 

## MQTT Broker
```shell
$ sudo apt-get update
$ sudo apt-get install mosquitto mosquitto-clients
$ sudo nano /etc/mosquitto/conf.d/default.conf
$ sudo systemctl restart mosquitto
```
`/etc/mosquitto/conf.d/defaultconf`
```
allow_anonymous false
password_file /etc/mosquitto/passwd

#tcp
#listener 1883 0.0.0.0

#websockets
listener 9083 0.0.0.0
protocol websockets
```
## 5g-modem start
```shell
$ cd Desktop/5g/Goonline
$ sudo ./simcom-cm
or to get a public IP address use
$ sudo ./simcom-cm -s vpn.telia.net
```
## 5g-modem AT commands
```shell
$ sudo apt-get install minicom
$ sudo minicom -D /dev/ttyUSB2
5g:
AT+CNMP=71
LTE:
AT+CNMP=38
```
## PC Client start
```shell
$ pip install -r requirements.txt
$ cd src
$ python mqtt_pc_client.py
```
## Raspberry pi client start
```shell
$ sudo chmod 666 /dev/ttyS0
$ pip install -r requirements.txt
$ cd src
$ python mqtt_raspberrypi.py
```

