import datetime
import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *

if __name__ == '__main__':
    print('Python receiver')

    hostname = 'localhost'
    port = 8888
    address = '1SNSR'

    pi = pigpio.pi('localhost', 8888)
    if not pi.connected:
        print('Not connected to Raspberry Pi')
        sys.exit()

    nrf = NRF24(pi, ce=25, payload_size=32, channel=76, data_rate=RF24_DATA_RATE.RATE_1MBPS, pa_level=RF24_PA.MIN)
    nrf.set_address_bytes(len(address))

    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)
    nrf.show_registers()

    try:
        print(f'Receiving from {address}')
        while True:
            while nrf.data_ready():
                pipe = nrf.data_pipe()
                payload = nrf.get_payload()
                # values = struct.unpack('<Lfb?', payload[:10])
                values = struct.unpack('<11s', payload[:11])
                print(values)
                print(''.join([str(v, 'UTF-8') for v in values]))
            time.sleep(1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()
