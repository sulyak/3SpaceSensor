from find_devices import display_devices
import api.threespace_api as tss

"""get all data from wired sensor

this is a test program to help test the interaction between unity and python
"""

def main():
    display_devices()

    dongles = []
    devices = tss.getComPorts()
    # finding all dongles
    for device in devices:
        if device.dev_type == "DNG":
            dongles.append(device)
    
    # assert that there is a dongle to work with
    if(not len(dongles)):
        print("please use a dongle")
        print("terminating the program...")
        return
    
    # connect with first dongle found
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
            
if __name__ == "__main__": main()