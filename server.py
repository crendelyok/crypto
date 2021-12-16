'''
The initial genesis account that holds genesis balance
During ICO it sends balances according to the number of capchas 
that every node solved

After ICO it chills
'''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

HOST = '127.0.0.1'

import argparse
from ctypes import OleDLL
from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
import p2p_nodes.blockchain_node as p2p
import time 

class Server():
    def __init__(self):
        self.server_node = p2p.BlockchainNode("127.0.0.1", 8001, 1)
    
    def start_server(self):
        self.server_node.start()
        return

    def stop_server(self):
        self.server_node.stop()
        return
        
    def print_connections(self):
        for node in self.server_node.all_nodes:
            print(node)
    
    def ICO(self):
        for node in self.server_node.all_nodes:
            message = { 'id' : node.id, 'ICO' : 5 }
            self.server_node.send_to_nodes(message) 
            # self.server_node.send_to_nodes("ICO")
            print(f'sent ICO: {message}')

def Test():
# Simple test of network connection
    # Initial Coin Offering
    server = Server()
    server.start_server()

    # every node that connected during sleep gets initial balance
    nodes = []
    for i in range(5):
        node = p2p.BlockchainNode(HOST, 8000 + i, 8000 + i)
        nodes.append(node)
        node.start()
        node.connect_with_node(HOST, 8001)
        node.send_to_nodes("I want initial coins!")
        
    time.sleep(1)
    server.print_connections()
    server.ICO()
    for node in nodes:
        node.stop()
    server.stop_server()
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_const', const = 1,  help='Test run')
    parser.add_argument('-n', action='store', help='Number of nodes to connect to perform ICO')
    args = parser.parse_args()

        
    # It flag -t is True
    if args.test is not None:
        Test()
        exit()

    # If no test performed
    # Initial Coin Offering
    server = Server()
    server.start_server()
    time.sleep(10) 

    # every node that connected during sleep gets initial balance
    server.print_connections()
    server.ICO()
    # except:
    #     print('ICO error!!!!!!!!!!!!!!!!!!!')


    # Server node now doesn`t do anything 
    # We use it for debugging and observing the net
    running = 1
    while running:
        print("Commands: stop")
        s = input("Please type a command:")

        if s == "stop":
            running = False
        else:
            print("Command not understood '" + s + "'")   


    server.stop_server()
    # print(app)
    # app.run(debug=True)
