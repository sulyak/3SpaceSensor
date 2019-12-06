import api.threespace_api as tss
import sys

"""this script pair one tss_dongle to one or more tss_wldevices
"""

WIRELESS_CHANNEL = 26
PAN_ID = 26
INDEX = 0

def main():
    devices = tss.getComPorts()
    print("%d device(s) found" % len(devices))
    if not len(devices):
        print("Zero devices found")
        return
    
    dongles = tss.getComPorts(tss.TSS_FIND_DNG)
    sensors = tss.getComPorts(tss.TSS_FIND_WL)

    if len(dongles) != 1:
        print("please use exactly one dongle")
        return
    if not len(sensors):
        print("please use at least one sensor")
        return

    print("\n")
    print("Changing Wireless Channels to %d" % WIRELESS_CHANNEL)
    print("Chaning PAN ID's to %d" % PAN_ID)
    print("Pairing sensor with index %d\n\n" % INDEX)
    print("press any key to continue...")
    input()

    true_dongle = tss.TSDongle(dongles[0].com_port)
    true_dongle.setWirelessPanID(PAN_ID)
    true_dongle.setWirelessChannel(WIRELESS_CHANNEL)
    
    for i, sensor in enumerate(sensors):
        true_sensor = tss.TSWLSensor(sensor.com_port)
        true_sensor.setWirelessPanID(PAN_ID)
        true_sensor.setWirelessChannel(WIRELESS_CHANNEL)

        # index of the paired list, default to zero
        true_dongle.setSensorToDongle(INDEX + i, true_sensor.serial_number)
        true_sensor.commitWirelessSettings()

    true_dongle.commitWirelessSettings()
    print("All done")

if __name__ == "__main__":
    try:
        int(sys.argv[1])
    except: pass
    else:
        INDEX = int(sys.argv[1])
    main()