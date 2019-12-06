import api.threespace_api as tss

def display_devices():
    devices = tss.getComPorts()
    print("%d device(s) found" % len(devices))
    if not len(devices): return

    for i, device in enumerate(devices):
            print("device #{}:".format(i + 1))
            print("type: {}".format(device.dev_type))
            print("port: {}".format(device.com_port))

def main():
    display_devices()


if __name__ == "__main__": main()