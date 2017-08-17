import time
import sys
import argparse
import bluetooth
import time
import json

from mindwave.bluetooth_headset import connect_magic, connect_bluetooth_addr
from mindwave.bluetooth_headset import BluetoothError

def mindwave_startup(view=None, description="", extra_args=[]):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('address', type=str, nargs='?',
                        const=None, default=None,
                        help="""Bluetooth Address of device. Use this
            if you have multiple headsets nearby or you want
            to save a few seconds during startup.""")
    for params in extra_args:
        name = params['name']
        del params['name']
        parser.add_argument(name, **params)
    args = parser.parse_args(sys.argv[1:])
    if args.address is None:
        socket = None
        retries = 0
        view.flash_message("Trying bluetooth connection...", "bluetooth")
        while socket is None and retries < 1:
            nearby = []
            try:
                socket, socket_addr, nearby = connect_magic()
            except:
                pass
            finally:
                if socket is None:
                    retries += 1
                    view.flash_message(json.dumps(nearby), "bluetooth")
                    view.flash_message("Retrying... {retries}".format(retries=retries), "bluetooth")
                    time.sleep(1)
                else: 
                    view.flash_message("MindWave Mobile found", "bluetooth")
        if socket is None:
            view.flash_message("No MindWave Mobile found.", "bluetooth")
            return None, None
    else:
        socket = connect_bluetooth_addr(args.address)
        if socket is None:
            view.flash_message("Connection failed.", "bluetooth")
            sys.exit(-1)
        socket_addr = args.address
    view.flash_message("Connected with MindWave Mobile at %s" % socket_addr, "bluetooth")
    for i in range(5):
        try:
            if i > 0:
                view.flash_message("Retrying...", "bluetooth")
            time.sleep(2)
            len(socket.recv(10))
            break
        except BluetoothError, e:
            print e
        if i == 5:
            view.flash_message("Connection failed.", "bluetooth")
            sys.exit(-1)
    return socket, args
