import argparse
from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
import p2p_nodes.blockchain_node as p2p
import time 

class Node():
    def __init__(self, port, id):
        self.node = p2p.BlockchainNode("127.0.0.1", port, id)

    def start_node(self):
        self.node.start()
        return

    def stop_node(self):
        self.node.stop()
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', action='store', help='Port number')
    parser.add_argument('-i', '--ico', action='store_const', const = 1,  help='ICO is running')
    args = parser.parse_args()
    assert args.port is not None
    

    # If ICO didn`t finished yet, we participate 
    if args.ico is not None:
        node = Node(int(args.port), int(args.port))
        node.start_node()

        node.node.connect_with_node('127.0.0.1', 8001)
        node.node.send_to_nodes("message: Hi there!")
        time.sleep(30)

        # Store initial couins
        # ...

    # Otherwise we connect to the net having 0 on the balance
    else:
        pass
        
    # Here the process of transactions begins
    # running = 1
    # while running:
    #     print("Commands: message, ping, discovery, status, connect, debug, stop")
    #     s = input("Please type a command:")

    #     if s == "stop":
    #         running = False

    #     elif s == "message":
    #         node.send_message(input("Message to send:"))

    #     elif s == "ping":
    #         node.send_ping()

    #     elif s == "discovery":
    #         node.send_discovery()

    #     elif s == "status":
    #         node.print_connections()

    #     elif s == "debug":
    #         node.debug = not node.debug

    #     elif ( s == "connect"):
    #         host = input("host: ")
    #         port = int(input("port: "))
    #         node.connect_with_node(host, port)

    #     else:
    #         print("Command not understood '" + s + "'")   


    node.stop_node()

    # print(app)
    # app.run(debug=True)
