import api.threespace_api as th

def main():
    devices = th.getComPorts()
    print("%d device(s) found" % len(devices))
    if not len(devices): return
    
    for i, device in enumerate(devices):
        print("device #%d:" % i + 1)
        print("type: {}".format(device.dev_type))
        print("port: {}".format(device.com_port))

if __name__ == "__main__": main()