"""Config and config-setup for the CatBus firmware."""

# pylint: disable=bare-except
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument

import machine


def _read_file(path, default):
    try:
        with open(path) as f:
            return f.read()
    except:
        return default


def _write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


class Config:
    def __init__(self):
        self.device_name = _read_file('catbus_device_name', '')
        self.mqtt_broker = _read_file('catbus_mqtt_broker', '')
        self.mqtt_topic = _read_file('catbus_mqtt_topic', '')

    def write(self):
        _write_file('catbus_device_name', self.device_name)
        _write_file('catbus_mqtt_broker', self.mqtt_broker)
        _write_file('catbus_mqtt_topic', self.mqtt_topic)

    def print(self):
        print('device name:  ' + self.device_name)
        print('MQTT broker:  ' + self.mqtt_broker)
        print('MQTT topic:   ' + self.mqtt_topic)


def choice(question):
    while True:
        answer = input(question + ' [y/n] ')
        if answer in ['y', 'n']:
            break
    return answer == 'y'


def edit():
    config = Config()

    config.print()
    print()

    changed = False

    while True:
        if choice('change device name?'):
            changed = True
            config.device_name = input('name: ')
            print()

        if choice('change MQTT broker?'):
            changed = True
            config.mqtt_broker = input('broker: ')
            print()

        if choice('change MQTT topic?'):
            changed = True
            config.mqtt_topic = input('topic: ')
            print()

        config.print()
        print()

        if choice('are these values OK?'):
            break
        else:
            print()

    if changed:
        config.write()

        if choice('restart now?'):
            machine.reset()
