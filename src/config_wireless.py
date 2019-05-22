import api.threespace_api as th

def main():
    devices = th.getComPorts()
    print("%d device(s) found" % len(devices))
    if not len(devices): return
    
    dongles = []
    sensors = []

    for i, device in enumerate(devices):
        print("device #{}:".format(i + 1))
        print("type: {}".format(device.dev_type))
        if device.dev_type == "WL": sensors.append(device)
        if device.dev_type == "DNG": dongles.append(device)

    print("\n\n")
    print("{} dongle(s) found".format(len(dongles)))
    for i, dongle in enumerate(dongles):
        true_dongle = th.TSDongle(dongle.com_port)
        print("dongle #{}".format(i))
        print("wireless channel: {}".format(true_dongle.getWirelessChannel()))
        print("PAN ID: {}".format(true_dongle.getWirelessPanID()))

    print("\n\n")
    print("{} sensor(s) found".format(len(sensors)))
    for i, sensor in enumerate(sensors):
        true_sensor = th.TSWLSensor(sensor.com_port)
        print("sensor #{}".format(i))
        print("wireless channel: {}".format(true_sensor.getWirelessChannel()))
        print("PAN ID: {}".format(true_sensor.getWirelessPanID()))

if __name__ == "__main__": main()