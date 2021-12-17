'''
The initial genesis account that holds genesis balance
During ICO it sends balances according to the number of capchas 
that every node solved

After ICO it chills
'''

import argparse
import p2p_nodes.blockchain_node as p2p
import time 
from configuration import *

class Server():
    def __init__(self):
        self.server_node = p2p.BlockchainNode(HOST, HOST_PORT, HOST_ID)
        
    def start_server(self):
        self.server_node.start()
        return

    def stop_server(self):
        self.server_node.stop()
        return
        
    def print_connections(self):
        print('\n')
        print('################################')
        print('All server connections')
        for node in self.server_node.all_nodes:
            print(node)
        print('################################')

    def ICO(self):
        for node in self.server_node.all_nodes:
            message = { 'id' : node.id, 'ICO' : 5, 'type' : 'ICO'}
            self.server_node.send_to_nodes(message) 
            print(f'sent ICO: {message}')

def Test_chain_alike_net():
# Simple test of chain-alike network connection
# 1 <- 2 <- 3 -< 4 ...
# This test checks if discovery works properly

    server = Server()
    server.start_server()

    nodes = []
    number_of_test_nodes = 20

    for i in range(number_of_test_nodes):
        node = p2p.BlockchainNode(HOST, HOST_PORT + 1 + i, HOST_PORT + 1 + i)
        nodes.append(node)
        node.start()
        time.sleep(1)
        node.connect_with_node(HOST, HOST_PORT + i)

    for node in nodes:
        node.send_discovery()
        # time.sleep(1)

    time.sleep(1)
    server.print_connections()
    server.ICO()

    # time.sleep(1)
    for node in nodes:
        print('\n')
        print('################################')
        print(f'All node {node.id} connections')
        for node_connection in node.all_nodes:
            print(node_connection)
        node.print_known_ids()
        print('################################')
        print('\n')

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
        Test_chain_alike_net()
        exit()

    # If no test performed
    # Initial Coin Offering
    server = Server()
    server.start_server()
    time.sleep(3) 

    # every node that connected during sleep gets initial balance
    server.print_connections()
    server.ICO()
    # except:
    #     print('ICO error!!!!!!!!!!!!!!!!!!!')


    # Server node now doesn`t do anything 
    # We use it for debugging and observing the net
    running = 1
    while running:
        print("Commands: [stop]")
        s = input("Please type a command:")
        if s == "s":
            running = False
        elif s == "show":
            for chain in server.server_node.all_blockchains:
                print('***************************')
                print(f'blockchain of {chain}')
                print(server.server_node.all_blockchains[chain])
                print('***************************')
        else:
            print("Command not understood '" + s + "'")   


    server.stop_server()