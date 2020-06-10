# Sonoff S20 firmware for CatBus

This is firmware for the Sonoff S20 IoT wall switch, to be controlled by CatBus.

Inside the Sonoff S20 is an ESP8266 connected to a button and a relay, and the serial pins are hooked up.
It is thus fairly easy to take apart and reflash with something else, in this case [MicroPython](http://micropython.org/).

The firmware:

- Uses the front button to toggle the switch on and off.
- Listens to an MQTT topic to turn the switch on and off.
- Publishes the state of the button to an MQTT topic when the button is pushed.

## Flashing

1. Install the _latest_ version of `esptool` from PIP.
   Don't use the version from APT, it's too out-of-date.
2. Erase the existing flash with `$ esptool.py --port /dev/ttyAMA0 erase_flash`, and hard reset the device.
3. Write the MicroPython firmware with `$ esptool.py --port /dev/ttyAMA0 --baud 406900 write_flash 0 micropython.bin`, and hard reset the device.
4. Connect to it with `$ screen /dev/ttyAMA0 115200`.
5. Press `C-b` to bring up the MicroPython prompt, and run `import webrepl_setup`, enabling it at boot.
   This allows you to update the firmware over WiFi.
6. Disable the WiFi Access Point (AP):

   ```python
   import network
   ap_if = network.WLAN(network.AP_IF)
   ap_if.active(False)
   ```

7. Enable the WiFi client:

   ```python
   import network
   sta_if = network.WLAN(network.STA_IF)
   sta_if.active(True)
   sta_if.scan()
   sta_if.connect('<essid>', '<password>')
   sta_if.isconnected()
   sta_if.ifconfig()
   ```
8. Copy `main.py` and `catbus.py` using [webrepl_cli](https://github.com/micropython/webrepl):

   ```sh
   $ python3 webrepl/webrepl_cli.py -p <password> main.py 192.168.16.42:/main.py
   $ python3 webrepl/webrepl_cli.py -p <password> catbus_config.py 192.168.16.42:/catbus_config.py
   ```

9. Run the `catbus_config` setup utility:

   ```python
   import catbus_config
   catbus_config.edit()
   ```

10. Reboot.

## Links

- [Tasmota](https://github.com/arendst/Tasmota) is an all-in-one firmware for such devices.
- [MicroPython docs for ESP8266](https://docs.micropython.org/en/latest/esp8266/quickref.html).
