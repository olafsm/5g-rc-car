# 5g-rc-car
5G-styrt bil. Eksperter i team prosjekt @NTNU

# Setup & install
```shell
$ sudo apt-get update
$ sudo apt-get install mosquitto mosquitto-clients
$ sudo nano /etc/mosquitto/conf.d/default.conf
$ sudo systemctl restart mosquitto
```
`/etc/conf.d/defaultconf`
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
```

## PC Client start
