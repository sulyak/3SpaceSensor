from find_devices import display_devices
import api.threespace_api as tss

"""get all data from wireless sensor through dongle
"""

def main():
    display_devices()

    # finding all dongles
    dongles = tss.getComPorts(filter=tss.TSS_FIND_DNG)
    
    # assert that there is a dongle to work with
    if len(dongles) != 1:
        print("please use exactly one dongle")
        print("terminating the program...")
        return
    
    # connect with dongle found
    true_dongle = tss.TSDongle(dongles[0].com_port)
    print("\n\nconnecting with dongle at com port %s..." % dongles[0].com_port)
    print("press any key to continue")
    input()

    true_device = true_dongle[0]
    if not true_device:
        print("no wireless sensors were found")
        print("terminating the program...")
        return

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
    true_device.close()
    true_dongle.close()
            
if __name__ == "__main__": main()