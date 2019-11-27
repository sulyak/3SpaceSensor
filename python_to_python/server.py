import sys
import zmq

def main():
    port = "5559"
    if len(sys.argv) > 1:
        port = sys.argv[1]
    
    # stabilish server
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)

    print("usage: python %s [port=5559]" % sys.argv[0])
    print("creating server tcp://127.0.0.1:%s" % port)

    while True:
        try:
            request = socket.recv()
            print("request received: %s " % request)
            print("what shall be the reply?")
            reply = input()
            socket.send_string(reply)
        except KeyboardInterrupt:
            break
    
    socket.close()




if __name__ == "__main__": main()