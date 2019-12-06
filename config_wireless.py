import api.threespace_api as tss
import sys

"""this script pair one tss_dongle to one or more tss_wldevices
"""

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

    # get information from dongle
    true_dongle = tss.TSDongle(dongles[0].com_port)
    wl_channel = true_dongle.getWirelessChannel()
    pan_id = true_dongle.getWirelessPanID()

    # get current index based on how many slots are left
    # TODO
    # index = true_dongle.getWirelessSlotsOpen()
    index = 0

    print("\n")
    print("Changing Wireless Channels to %d" % wl_channel)
    print("Chaning PAN ID's to %d" % pan_id)
    print("Pairing sensor with index %d\n\n" % index)
    print("press any key to continue...")
    input()

    for i, sensor in enumerate(sensors):
        true_sensor = tss.TSWLSensor(sensor.com_port)
        true_sensor.setWirelessPanID(pan_id)
        true_sensor.setWirelessChannel(wl_channel)

        # index of the paired list, default to zero
        true_dongle.setSensorToDongle(index + i, true_sensor.serial_number)
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