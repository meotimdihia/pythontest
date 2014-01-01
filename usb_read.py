import usb.core
import usb.util
import time
from pprint import pprint

VENDOR_ID = 0x0B38
PRODUCT_ID = 0x0010

# find the USB device
device = usb.core.find(idVendor=VENDOR_ID,
                       idProduct=PRODUCT_ID)
if device != None:
    # use the first/default configuration
    device.set_configuration()
    #pprint(vars(device))
    #pprint(vars(device.get_active_configuration()))
    # first endpoint
    endpoint = device[0][(0,0)][0]

    # read a data packet
    attempts = 10
    data = None


    while data == None and attempts > 0:
        try:

            data = device.read(endpoint.bEndpointAddress,
                               endpoint.wMaxPacketSize, 0, 100)
            print 'Reading...'
        except usb.core.USBError as e:
            data = None
            if e.args == ('Operation timed out',):
                print 1
                attempts -= 1
                continue
        time.sleep(.10)

    sret = ''.join([chr(x) for x in data])
    print sret
else:
    print 'Can not find this device'