import usb
busses = usb.busses()

for bus in busses:
    for dev in bus.devices:
        try:
            print ("iManufacturer   : %s" % usb.util.get_string(dev.dev, 256, 1))
            print ("iProduct            : %s" % usb.util.get_string(dev.dev, 256, 2))
            print ("iSerialNumber   : %s" % usb.util.get_string(dev.dev, 256, 3))
        except Exception, ex:
            pass

