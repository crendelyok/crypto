import argparse
import p2p_nodes.blockchain_node as p2p
import time 
from configuration import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', action='store', help='Port number')
    parser.add_argument('-i', '--ico', action='store_const', const = 1,  help='ICO is running')
    args = parser.parse_args()
    if args.port is None:
        print(bcolors.FAIL + 'Please specify port using "-p port_number"' + bcolors.ENDC)
        assert args.port is not None

    # If ICO didn`t finished yet, we participate 
    if args.ico is not None:
        node = p2p.BlockchainNode(HOST, int(args.port))
        node.start()

        node.connect_with_node(HOST, HOST_PORT)
        node.send_to_nodes("I want initial coins!")
        time.sleep(10)

        # Store initial coins
        # ...

    # Otherwise we connect to the net having 0 on the balance
    else:
        pass
        
    # Here the process of transactions begins
    running = 1
    print("Commands: message, ping, discovery, status, connect, debug, stop")
    while running:
        
        s = input("Please type a command:\n")

        if s == "stop":
            running = False

        elif s == "message":
            node.send_message(input("Message to send:\n"))

        elif s == "ping":
            node.send_ping()

        elif s == "discovery":
            node.send_discovery()

        elif s == "status":
            node.print_connections()

        elif s == "debug":
            node.debug = not node.debug

        elif ( s == "connect"):
            host = input("host: ")
            port = int(input("port: "))
            node.connect_with_node(host, port)

        else:
            print("Command not understood '" + s + "'")   


    node.stop()