from find_devices import display_devices
import api.threespace_api as tss
import matplotlib.pyplot as plt
import psutil
import time


def main():
    display_devices()

    wired = []
    devices = tss.getComPorts()
    # finding all wired sensors
    # TODO add compatibility with dongles
    for device in devices:
        if device.dev_type == "WL":
            wired.append(device)
    
    # assert that there is a wired sensor to work with
    if(not len(wired)):
        print("please use a wired wireless sensor")
        print("terminating the program...")
        return
    
    # connect with first device found
    true_device = tss.TSWLSensor(wired[0].com_port)
    print("\n\nconnecting with device at com port %s..." % wired[0].com_port)
    print("press any key to continue")
    input()


    figure = plt.figure()
    ax = figure.add_subplot(111)
    figure.show()

    i = 0
    x, y = [], []

    while True:
        x.append(i)
        y.append(true_device.getCorrectedGyroRate())

        ax.plot(x, y, color="blue")
        figure.canvas.draw()
        ax.set_xlim(left=max(0, i-50), right=i+50)
        plt.pause(.005)
        i += 1

if __name__ == "__main__":
    main()