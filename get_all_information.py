from find_devices import display_devices
import api.threespace_api as tss

"""get all data from wired sensor

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
    
    # connect with first device found
    true_device = tss.TSWLSensor(wired[0].com_port)
    print("\n\nconnecting with device at com port %s..." % wired[0].com_port)
    print("press any key to continue")
    input()

    # getting all data from sensor until CTRL-C is pressed
    try:
        while True:
            data = true_device.getAllRawComponentSensorData()
            out = "[%f, %f, %f] --Gyro\n"\
                  "[%f, %f, %f] --Accel\n"\
                  "[%f, %f, %f] --Comp" % data
            print(out)
    except KeyboardInterrupt:
        print("stopped")
            
if __name__ == "__main__": main()