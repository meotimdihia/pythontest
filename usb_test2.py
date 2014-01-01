#!/usr/bin/python
"""
You must be using the new PyUSB 1.0 branch and not the 0.x branch.

Copyright (c) 2011 - Bernard `Guyzmo` Pratz - guyzmo{at}hackable-devices{dot}org
Forked from: Copyright (c) 2010 - Micah Carrick - http://www.micahcarrick.com/credit-card-reader-pyusb.html

Modified by : meotimdihia
"""
import sys
import usb.core
import usb.util
import time

VENDOR_ID = 0x0B38
PRODUCT_ID = 0x0010
DATA_SIZE = 167

# keycode mapping
key_pages = [
'', '', '', '',
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\n', '^]', '^H',
'^I', ' ', '-', '=', '[', ']', '\\', '>', ';', "'", '`', ',', '.',
'/', 'CapsLock', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
'PS', 'SL', 'Pause', 'Ins', 'Home', 'PU', '^D', 'End', 'PD', '->', '<-', '-v', '-^', 'NL',
'KP/', 'KP*', 'KP-', 'KP+', 'KPE', 'KP1', 'KP2', 'KP3', 'KP4', 'KP5', 'KP6', 'KP7', 'KP8',
'KP9', 'KP0', '\\', 'App', 'Pow', 'KP=', 'F13', 'F14' ]

key_pages_shift = [
'', '', '', '',
'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
'!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '\n', '^]', '^H',
'^I', ' ', '_', '+', '{', '}', '|', '<', ':', '"', '~', '<', '>',
'?', 'CapsLock', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
'PS', 'SL', 'Pause', 'Ins', 'Home', 'PU', '^D', 'End', 'PD', '->', '<-', '-v', '-^', 'NL',
'KP/', 'KP*', 'KP-', 'KP+', 'KPE', 'KP1', 'KP2', 'KP3', 'KP4', 'KP5', 'KP6', 'KP7', 'KP8',
'KP9', 'KP0', '|', 'App', 'Pow', 'KP=', 'F13', 'F14' ]

def map_character(c):
    #return keymap[keycode[c]]
    return key_pages[c]

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        print n
        yield l[i:i+n]
a = ['B', [1, 0, 6, 0, 0, 0, 0, 0]]
map_keys = lambda c: key_pages_shift[c[1]] if c[0] is 2 else key_pages[c[1]]
# print "".join(map(map_keys, [(d[0], d[2]) for d in chunks(a, 8)]))

class MagSwipe:
    def __init__(self):
        # find the MagSwipe reader
        device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        self._device = device

        if device is None:
            sys.exit("Could not find MagTek USB HID Swipe Reader.")

        # make sure the hiddev kernel driver is not active
        # if device.is_kernel_driver_active(0):
        #     try:
        #         device.detach_kernel_driver(0)
        #     except usb.core.USBError as e:
        #         sys.exit("Could not detatch kernel driver: %s" % str(e))

        # set configuration
        try:
            pass
            #device.set_configuration()
            #device.reset()
        except usb.core.USBError as e:
            sys.exit("Could not set configuration: %s" % str(e))

        self._endpoint = device[0][(0,0)][0]

    def wait_for_swipe(self):
        # wait for swipe
        data = []
        swiped = False

        print self._device
        
        print 'endpoint %s' % self._endpoint
        print "Please type a key on keyboard..."

        while 1:
            try:

                data = self._device.read(self._endpoint.bEndpointAddress, self._endpoint.wMaxPacketSize)

                if not swiped:
                    print "Reading..."
                swiped = True
                print data
                print "Data: %s" % ''.join(map(chr, data))
                sret = ''.join([chr(x) for x in data])
                print sret
                map_keys = lambda c: key_pages_shift[c[1]] if c[0] is 2 else key_pages[c[1]]
                data = "".join(map(map_keys, [(d[0], d[2]) for d in chunks(data, 8)]))
                print "key: " . data
            except usb.core.USBError as e:
                if e.args[0] == 110 and swiped:
                    if len(data) < DATA_SIZE:
                        print "Bad swipe, try again. (%d bytes)" % len(data)
                        print "Data: %s" % ''.join(map(chr, data))
                        data = []
                        swiped = False
                        continue
                    else:
                        break   # we got it!

        # convert text
        map_keys = lambda c: key_pages_shift[c[1]] if c[0] is 2 else key_pages[c[1]]
        data = "".join(map(map_keys, [(d[0], d[2]) for d in chunks(data, 8)]))
        time.sleep(.01)
        return data

if __name__ == "__main__":
    print MagSwipe().wait_for_swipe()