import zmq

PORT = "5551"

def main():
    # connect to server
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    # couldnt use 'tcp://*:5551' 
    socket.connect("tcp://127.0.0.1:%s" % PORT)

    message = input("send a message:")
    socket.send_string(message)

    reply = socket.recv()
    print("message replyed with %s" % reply)




if __name__ == "__main__": main()