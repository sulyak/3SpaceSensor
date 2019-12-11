from find_devices import display_devices
import api.threespace_api as tss
import time

import sqlite3 as sql

# debug
import db_parser
import importlib

import db

"""get wireless data from sensor 
and saves in a database 
"""


def main():
    display_devices()

    # finding all dongles
    dongles = tss.getComPorts(tss.TSS_FIND_DNG)

    # assert that there is a dongle to work with
    if len(dongles) != 1:
        print("please use exaclty one dongle")
        print("terminating the program...")
        input()
        return
    
    # connect with dongle found
    true_dongle = tss.TSDongle(dongles[0].com_port)
    print("\n\nconnecting with dongle at com port %s..." % dongles[0].com_port)
    print("press any key to continue")
    input()

    # get the wireless sensors paired to the dongle
    true_devices = []
    for true_device in true_dongle:
        # print(true_device)
        if true_device: true_devices.append(true_device)

    # make sure that there are sensor to work with
    if not len(true_devices):
        print("no wireless sensor found")
        print("terminating the program")
        input()
        return

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
    countdown(3)
    
    generate_table(true_devices, t_len=-1)
    print("stopped")

def generate_table(devices, t_len=10):
    con = db.init("TSS.db")
    cursor = con.cursor()

    function_names = ["getRawGyroscopeRate", "getRawAccelerometerData", "getRawCompassData"]
    try:
        # run the recording for t_len seconds
        t_end = time.time() + t_len
        while time.time() < t_end or t_len == -1: # -1 debug tool for endless record
            # this is the mode with all 3 other function
            row = []
            for device in devices:
                for func_name in function_names:
                    for data in getattr(device, func_name)():
                        row.append(data)
            time.sleep(.5)

            # deal with the data collected
            importlib.reload(db_parser)
            try:
                query = db_parser.parse_to_query(row)
            except Exception as e:
                print(e)
            else:
                cursor.execute(query)

    except KeyboardInterrupt:
        print("stopped")

    con.commit()


def countdown(seconds):
    for i in reversed(range(seconds)):
        print(str(i + 1) + "...")
        time.sleep(1)
    print("GO!")

if __name__ == "__main__": main()
