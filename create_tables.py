from find_devices import display_devices
import api.threespace_api as tss
import time

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
    if not len(dongles):
        print("please use a dongle")
        print("terminating the program...")
        return
    
    # connect with first dongle found
    true_dongle = tss.TSDongle(dongles[0].com_port)
    print("\n\nconnecting with dongle at com port %s..." % dongles[0].com_port)
    print("press any key to continue")
    input()

    # get the wireless sensors paired to the dongle
    true_devices = []
    for true_device in true_dongle:
        # print(true_device)
        if true_device: true_devices.append(true_device)

    print("using %d wireless device(s)" % len(true_devices))
    print("press any key to continue...")
    input()   

    # get the length of the recording in seconds
    print("how long should the recording be? (3 - 60) in seconds")
    t_len = input()
    try: t_len = int(t_len)
    except: t_len = 3
    if 3 < t_len > 60: t_len = 3
    print("recording for %d seconds..." % t_len)
    time.sleep(2)

    
    generate_table(true_devices, 3, t_len=t_len)

def generate_table(devices, mode, t_len=10):
    """
    0 - gyro
    1 - accel
    2 - compass
    3 - all of the above
    """
    if mode not in range(4): return
    file_name = ["gyro", "accel", "comp", "all_data"]
    fp = open("table_" + file_name[mode] + ".txt", "w")

    function_name = ["getRawGyroscopeRate", "getRawAccelerometerData", "getRawCompassData"]
    try:
        # run the recording for t_len seconds
        t_end = time.time() + t_len
        while time.time() < t_end:
            if mode != 3:
                line = ""
                for i, device in enumerate(devices):
                    # this way we can call a function using its name as a string
                    function = getattr(device, function_name[mode])
                    # separate the items with an empty column (separating output from diffrent devices)
                    if i: line += ",,"
                    line += "%.03f,%.03f,%.03f" % function()
                line += ";\n"
                fp.writelines(line)
                print(line, end='')
            else:
                # this is the mode with all 3 other function
                for j, func_name in enumerate(function_name):
                    line = ""
                    for i, device in enumerate(devices):
                        function = getattr(device, func_name)
                        if not i:
                            line += file_name[j]
                        line += ",,%.03f,%.03f,%.03f" % function()
                    line += ";\n"
                    fp.writelines(line)
                    print(line, end='')
                fp.writelines("\n")

    except KeyboardInterrupt:
        print("stopped")

    fp.close()

if __name__ == "__main__": main()