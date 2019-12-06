from find_devices import display_devices
import api.threespace_api as tss

"""get all data from wired sensor
"""

def main():
    display_devices()

    # finding all wired sensors
    wired = tss.getComPorts(filter=tss.TSS_FIND_WL)
    
    # assert that there is a wired sensor to work with
    if len(wired) != 1:
        print("please use exactly one wired wireless sensor")
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
            out = "--Gyro  [%f, %f, %f] \n"\
                  "--Accel [%f, %f, %f] \n"\
                  "--Comp  [%f, %f, %f] \n" % data
            print(out)
    except KeyboardInterrupt:
        print("stopped")
            
if __name__ == "__main__": main()