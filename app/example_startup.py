import time
import sys
import argparse
import bluetooth
import time

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
        while socket is None and retries < 2:
            try:
                socket, socket_addr = connect_magic()
            except:
                retries += 1
                view.print_message("Retrying... {retries}".format(retries=retries))
                time.sleep(1)
        if socket is None:
            view.print_message("No MindWave Mobile found.")
            return None, None
    else:
        socket = connect_bluetooth_addr(args.address)
        if socket is None:
            view.print_message("Connection failed.")
            sys.exit(-1)
        socket_addr = args.address
    print "Connected with MindWave Mobile at %s" % socket_addr
    for i in range(5):
        try:
            if i > 0:
                view.print_message("Retrying...")
            time.sleep(2)
            len(socket.recv(10))
            break
        except BluetoothError, e:
            print e
        if i == 5:
            view.print_message("Connection failed.")
            sys.exit(-1)
    return socket, args
