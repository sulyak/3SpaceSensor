from find_devices import display_devices
import api.threespace_api as tss

"""get gyro date from wired sensor

this is a test program to help test the interaction between unity and python
"""

def main():
    display_devices()

    wired = []
    devices = tss.getComPorts()
    # finding all wired sensors
    # TODO add compatibility with dongles
    for device in devices:
        if device.dev_type == "WL":
            wired.append(device)
    
    # assert that there is a wired sensor to work with
    if(not len(wired)):
        print("please use a wired wireless sensor")
        print("terminating the program...")
        return
    
    true_device = tss.TSWLSensor(wired[0].com_port)
    print("\n\nconnecting with device at com port %s..." % wired[0].com_port)
    print("press any key to continue")
    input()

    try:
        while True:
            print("%.2f %.2f %.2f" % true_device.getRawGyroscopeRate())
    except KeyboardInterrupt:
        print("stopped")
            
if __name__ == "__main__": main()