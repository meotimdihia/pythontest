import usb.core
import usb.util
import usb.backend
import sys
import time

VENDOR_ID = 0x10c4 # nhiet do
PRODUCT_ID = 0xea60

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
# was it found?
if dev is None:
    raise ValueError('Device not found')



# cfg = usb.util.find_descriptor(dev)
# cfg.set()
# dev.set_configuration(cfg)
# dev.reset()

endpoint = dev[0][(0,0)][0]
print endpoint
#make sure the hiddev kernel driver is not active

try:
    if dev.is_kernel_driver_active(0):
        print "detaching device..."
        dev.detach_kernel_driver(0)
except usb.core.USBError as e:
    sys.exit("Could not detatch kernel driver: %s" % str(e))
dev.set_configuration()


# dev.ctrl_transfer(0xC1, 0xB, 0x1FD, 0, 0)
# data = dev.ctrl_transfer(0xC1,0x10,0x310B,0, 0x14)
# print data

# for bRequest in range(255):
#     try:
#         data = dev.ctrl_transfer(0xC0,0xFF,0x370B,0, 0x1)
#         # ret = dev.ctrl_transfer(0xC0, bRequest, 0, 0, 1)
#         print "bRequest ",bRequest
#         print ret
#     except:
#         # failed to get data for this request
#         pass

# while True:
#     data = dev.ctrl_transfer(0xC1,0x10,0x0,0x0,14)
#     print data
#     time.sleep(1)



data = dev.ctrl_transfer(0xC0,0xFF,0x370B,0x0, 0x1)

data = dev.ctrl_transfer(0x41,0x0,0x1,0x0)

data = dev.ctrl_transfer(0xC1,0x8,0x0,0x0,0x1)

data = dev.read(0x81, endpoint.wMaxPacketSize, 0, 0x0)


dev.ctrl_transfer(0xC1,0x8,0x0,0x0,0x4) # In 00

dev.ctrl_transfer(0x41,0x0B,0x01FD,0x0) # Out

dev.ctrl_transfer(0x41,0x12,0xF,0x0) # Out

dev.ctrl_transfer(0x41,0x0B,0x1FD,0x0) # Out
 
dev.ctrl_transfer(0x41,0x0B,0x1FD,0x0) # Out

# Get temperature and wind speed 
dev.ctrl_transfer(0x41,0x1E,0x1FD,0x0, [0x80, 0x25, 0x0, 0x0]) # Out 80 25 00 00
 
dev.ctrl_transfer(0x41,0x07,0x0202,0x0) # Out
 
dev.ctrl_transfer(0x41,0x07,0x101,0x0) # Out
 
dev.ctrl_transfer(0x41,0x03,0x800,0x0) # Out
 
dev.ctrl_transfer(0x41,0x19,0x0,0x0, [0x1A, 00, 00, 00, 0x11, 0x13]) # Out
 
dev.ctrl_transfer(0x41,0x13,0x0,0x0, [0x1, 00, 00, 00, 0x4, 00, 00, 00, 0x01, 00, 00, 00, 0x01, 00, 00]) # Out
 
dev.ctrl_transfer(0xC1,0x8,0x0,0x0,0x2) # In 03
 
dev.ctrl_transfer(0xC1,0x8,0x0,0x0,0x2) # In 03
 
dev.ctrl_transfer(0xC1,0x8,0x0,0x0,0x2) # In 03
 
dev.ctrl_transfer(0xC1,0x8,0x0,0x0,0x2) # In 03
 
dev.ctrl_transfer(0xC1,0x10,0x0,0x0,0x14) # In 08, 00, ...
 
dev.ctrl_transfer(0xC1,0x8,0x0,0x0,0x2) # In 03
 
dev.ctrl_transfer(0xC1,0x8,0x0,0x0,0x2) # In 03
 
dev.ctrl_transfer(0xC1,0x8,0x0,0x0,0x2) # In 03
 
dev.ctrl_transfer(0xC1,0x8,0x0,0x0,0x2) # In 03

dev.read(0x81, endpoint.wMaxPacketSize, 0, 1000) # 1 bytes 00
 
dev.read(0x81, endpoint.wMaxPacketSize, 0, 1000) # 512 bytes = 0x200 
 
dev.ctrl_transfer(0x41,0x0B,0x01FD,0x0) # Out
 
dev.ctrl_transfer(0xC1,0x10,0x0,0x0,0x14) # In 04, 00, 00, 00, 00, 00, 00, 01, 00 ....

block = []
while True: 
    # data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 0, 0x0) # 1 bytes 00
         
    data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 0, 100) # 512 bytes = 0x200
    print data
    # n = 0
    # for i,v in enumerate(data):
    #     # check "i" is first character or not continue to loop

    #     if not block and v != 0:
    #         continue
    #     elif i+1 == len(data):
    #         continue
    #     elif data[i+1] == 0:
    #         continue


    #     block.append(v)
    #     if (len(block) == 13):
    #         print block
    #         block[2] # humidity
    #         block[7] # temperature
    #         block[8] # mode (unit) windspeed
    #         block[9] # change way to show windspeed
    #         block[10] # windspeed number
    #         block[11] # decimal wind speed ?
    #         block = []

    time.sleep(0.4)

# data = dev.ctrl_transfer(0xC1,0x8,0x0,0x0,1)
# print data


# data = dev.ctrl_transfer(0xC1,0x8,0x0,0x0,4)
# print data

# data = dev.ctrl_transfer(0x41,0x0B,0x1FD,0x0)
# print data

# data = dev.ctrl_transfer(0x41,0x12,0xF,0x0)
# print data

# data = dev.ctrl_transfer(0x41,0x0B,0x1FD,0x0)
# print data

# data = dev.ctrl_transfer(0x41,0x0B,0x1FD,0x0, [128, 37, 0, 0])
# print data
# data = dev.ctrl_transfer(0x41,0x0B,0x1FD,0x0, [])
# print data
# while True:
#     # data = dev.ctrl_transfer(0x41,0x19,0x1FD,0x0, [26, 0, 0, 0, 17, 19])
#     # print data

#     # data = dev.ctrl_transfer(0x41,0x13,0x1FD,0x0, [1, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0])
#     # print data
#     # data = dev.ctrl_transfer(0xC1,0x10,0x0,0x0, 0x14)
#     # print data
#     # data = dev.ctrl_transfer(0xC1,0x8,0x0,0x0, 2)
#     # print data
#     dev.set_configuration()
#     data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 0, 100)
#     print data 


# data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 0, 100000)
# print data 

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

