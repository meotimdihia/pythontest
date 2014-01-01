import usb
import pprint
#help(usb.core) 
busses = usb.busses()

pp = pprint.PrettyPrinter(indent=4)

for bus in busses:
  devices = bus.devices

  for dev in devices:
    try:
        print ("iManufacturer   : %s" % usb.util.get_string(dev.dev, 256, 1))
        print ("iProduct            : %s" % usb.util.get_string(dev.dev, 256, 2))
        print ("iSerialNumber   : %s" % usb.util.get_string(dev.dev, 256, 3))    
        print "Device:", dev.filename
        print "  Device class:",dev.deviceClass
        print "  Device sub class:",dev.deviceSubClass
        print "  Device protocol:",dev.deviceProtocol
        print "  Max packet size:",dev.maxPacketSize
        print "  idVendor:",hex(dev.idVendor)
        print "  idProduct:",hex(dev.idProduct)
        print "  Device Version:",dev.deviceVersion
        for config in dev.configurations:
          print "  Configuration:", config.value
          print "    Total length:", config.totalLength 
          print "    selfPowered:", config.selfPowered
          print "    remoteWakeup:", config.remoteWakeup
          print "    maxPower:", config.maxPower
          for intf in config.interfaces:
            print "    Interface:",intf[0].interfaceNumber
            for alt in intf:
              print "    Alternate Setting:",alt.alternateSetting
              print "      Interface class:",alt.interfaceClass
              print "      Interface sub class:",alt.interfaceSubClass
              print "      Interface protocol:",alt.interfaceProtocol
              for ep in alt.endpoints:
                print "      Endpoint:",hex(ep.address)
                print "        Type:",ep.type
                print "        Max packet size:",ep.maxPacketSize
                print "        Interval:",ep.interval
    except Exception, msg:
        pass

def turn_on_off_mouse():
    if dev is None:
        print "device not found"
    else:
        print "device found"

    if dev.is_kernel_driver_active(interface) is True:
        print "but we need to detach kernel driver"
        dev.detach_kernel_driver(interface)

    print "claiming device"
    usb.util.claim_interface(dev, interface)
    print "release claimed interface"
    usb.util.release_interface(dev, interface)
    print "now attaching the kernel driver again"
    dev.attach_kernel_driver(interface)
    print "all done"
    
    return 0