import usb.core
import usb.util
import usb.backend
import sys
VENDOR_ID = 0x10c4 # nhiet do
PRODUCT_ID = 0xea60
def main():
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)


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

#make sure the hiddev kernel driver is not active
    if dev.is_kernel_driver_active(0):
        try:
            print "detaching device..."
            dev.detach_kernel_driver(0)
        except usb.core.USBError as e:
            sys.exit("Could not detatch kernel driver: %s" % str(e))

    dev.ctrl_transfer(0x40,0x09,0,0x05,[96,9,0,0,3])

    dev.set_configuration()

    endpoint = dev[0][(0,0)][0]
    
    blank = False
    raw = False
    while True:
        print 2

        data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, 0 , 1000)
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

main()