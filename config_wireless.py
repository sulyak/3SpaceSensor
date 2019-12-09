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
    # 15 is the max slots per dongle
    index = 15 - true_dongle.getWirelessSlotsOpen()

    print("\n")
    print("Changing Wireless Channels to %d" % wl_channel)
    print("Chaning PAN ID's to %d" % pan_id)
    print("Pairing sensor with index %d\n\n" % index)
    print("press any key to continue...")
    input()

    for sensor in sensors:
        if not true_dongle.getWirelessSlotsOpen():
            print("dongle reached its max capacity")
            break

        # connect to the sensor
        true_sensor = tss.TSWLSensor(sensor.com_port)
        # wireless settings
        true_sensor.setWirelessPanID(pan_id)
        true_sensor.setWirelessChannel(wl_channel)

        # pairing the sensor to the dongle
        # index of the paired list, default to zero
        true_dongle.setSensorToDongle(index, true_sensor.serial_number)
        index += 1

        true_sensor.commitWirelessSettings()


    true_dongle.commitWirelessSettings()
    true_dongle.close()
    print("All done")

if __name__ == "__main__": main()