# Sonoff S20 firmware for CatBus

This is firmware for the Sonoff S20 IoT wall switch, to be controlled by CatBus.

Inside the Sonoff S20 is an ESP8266 connected to a button and a relay, and the serial pins are hooked up.
It is thus fairly easy to take apart and reflash with something else, in this case [MicroPython](http://micropython.org/).

The firmware:

- Uses the front button to toggle the switch on and off.
- Listens to an MQTT topic to turn the switch on and off.
- Publishes the state of the button to an MQTT topic when the button is pushed.

## Links

- [Tasmota](https://github.com/arendst/Tasmota) is an all-in-one firmware for such devices.
- [MicroPython docs for ESP8266](https://docs.micropython.org/en/latest/esp8266/quickref.html).
