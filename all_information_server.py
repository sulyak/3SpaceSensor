from find_devices import display_devices

import api.threespace_api as tss
import zmq

"""get all data from wired sensor and send to unity

this is a test program to help test the interaction between unity and python

this file is similar to get_all_information.py 
"""

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

    # connect to server
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5559")

    try:
        while True:
            message = socket.recv()
            print("request received: %s" % message)

            # TODO diffrent answers from diffrent requests
            if(message == b"getAllData"):
                data = true_device.getAllRawComponentSensorData()
                out = "[%.2f, %.2f, %.2f] --Gyro\n"\
                    "[%.2f, %.2f, %.2f] --Accel\n"\
                    "[%.2f, %.2f, %.2f] --Comp" % data
                print("sending:\n" + out)

                socket_out = "%.2f, %.2f, %.2f\n"\
                    "%.2f, %.2f, %.2f\n"\
                    "%.2f, %.2f, %.2f" % data
                socket.send_string(out)
            else:
                socket.send_string("unrecognized request")
    except KeyboardInterrupt:
        print("stopped")
            
if __name__ == "__main__": main()