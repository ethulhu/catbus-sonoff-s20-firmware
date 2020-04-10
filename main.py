"""Put a Sonoff S20 onto CatBus."""

# pylint: disable=bare-except
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument

import time

import machine
import umqtt.simple as umqtt

import catbus_config


class Button(machine.Pin):
    """An input button that calls a callback when pressed."""

    def __init__(self, pin, callback=None):
        if not callback:
            raise ValueError('callback must not be None')

        super().__init__(pin, machine.Pin.IN)

        timer = machine.Timer(0)

        # the timer callback needs a parameter, so this just consumes that.
        def _callback(timer):
            callback()

        def debounce_button(pin):
            timer.init(mode=timer.ONE_SHOT, period=200, callback=_callback)

        self.irq(trigger=machine.Pin.IRQ_RISING, handler=debounce_button)


class Relay(machine.Pin):
    """An output relay."""

    def __init__(self, pin):
        super().__init__(pin, machine.Pin.OUT)

    def toggle(self):
        if self.value() == 0:
            self.on()
        else:
            self.off()

    def value_catbus(self):
        return b'on' if self.value() else b'off'


def main():
    config = catbus_config.Config()

    if not config.device_name:
        # We haven't been set up and can't do anything.
        return

    topic = config.mqtt_topic.encode('utf-8')

    relay = Relay(12)

    def on_message(topic, data):
        if data == b'on':
            relay.on()
        elif data == b'off':
            relay.off()
        else:
            pass

    mqtt = umqtt.MQTTClient(config.device_name, config.mqtt_broker)
    mqtt.set_callback(on_message)
    mqtt.connect()
    mqtt.subscribe(topic, qos=1)

    def on_button_pressed():
        relay.toggle()
        mqtt.publish(topic, relay.value_catbus(),
                     retain=True, qos=1)

    button = Button(0, callback=on_button_pressed)

    while True:
        try:
            mqtt.wait_msg()
        except:
            mqtt.connect()
            mqtt.subscribe(topic, qos=1)
            time.sleep(1)


main()
