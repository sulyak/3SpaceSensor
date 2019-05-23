import zmq

PORT = "5551"

def main():
    # stabilish server
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % PORT)

    while True:
        request = socket.recv()
        print("request received: %s " % request)
        print("what shall be the reply?")
        reply = input()
        socket.send_string(reply)




if __name__ == "__main__": main()