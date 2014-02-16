import usb.core
import usb.util
import usb.backend
import sys
import time

VENDOR_ID = 0x05ac # nhiet do
PRODUCT_ID = 0x12a0

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
# was it found?
if dev is None:
    raise ValueError('Device not found')

dev.set_configuration()

endpoint = dev[0][(0,0)][0]

while True:
    # data = dev.ctrl_transfer(0x41,0x19,0x1FD,0x0, [26, 0, 0, 0, 17, 19])
    # print data
    data = dev.ctrl_transfer(0xC0, 0x45, 0, 0, 1)
    print data
    # data = dev.ctrl_transfer(0x41,0x13,0x1FD,0x0, [1, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0])
    # print data
    # data = dev.ctrl_transfer(0xC1,0x10,0x0,0x0, 0x14)
    # print data
    # data = dev.ctrl_transfer(0xC1,0x8,0x0,0x0, 2)
    # print data
    dev.set_configuration()
    data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 0, 3000)
    print data 
    time.sleep(1)

data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 0, 100000)
print data 

# blank = False
# raw = False
# while True:
#     print "End Point: %s" % endpoint.bEndpointAddress

#     data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 0, 1000)
#     print 1
#     if raw == True:
#         print(data)
#     elif data[0] != 240:
#         line = ""
#         for value in data:
#             line += str(value) + " " * (4 - len(str(value)))
#         print(line)
#         blank = False
#     elif blank == False:
#         blank = True
#         print("")

