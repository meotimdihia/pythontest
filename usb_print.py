import usb.core
import usb.util
import usb.backend
import sys
VENDOR_ID = 0x10c4 # nhiet do
PRODUCT_ID = 0xea60

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
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
        
#make sure the hiddev kernel driver is not active
if dev.is_kernel_driver_active(0):
    try:
        print "detaching device..."
        dev.detach_kernel_driver(0)
    except usb.core.USBError as e:
        sys.exit("Could not detatch kernel driver: %s" % str(e))

if dev is None:
    raise ValueError('Device not found')
else:
    print("Device found")


# dev.ctrl_transfer(0xC1, 0xB, 0x1FD, 0, 0)
data = dev.ctrl_transfer(0xC1,0x10,0x310B,0, 0x14)
print data

data = dev.ctrl_transfer(0xC0,0xFF,0x310B,0, 0x14)
print data

map_keys = lambda c: key_pages_shift[c[1]] if c[0] is 2 else key_pages[c[1]]
data = "".join(map(map_keys, [(d[0], d[2]) for d in chunks(data, 8)]))
print "key: " + data

data = dev.ctrl_transfer(0x41,0x03, 0x0800, 0x0000, 0x0000)
print data

# dev.set_configuration()

endpoint = dev[0][(0,0)][0]

blank = False
raw = False
while True:
    print "End Point: %s" % endpoint.bEndpointAddress

    data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 0, 1000)
    print 1
    if raw == True:
        print(data)
    elif data[0] != 240:
        line = ""
        for value in data:
            line += str(value) + " " * (4 - len(str(value)))
        print(line)
        blank = False
    elif blank == False:
        blank = True
        print("")

