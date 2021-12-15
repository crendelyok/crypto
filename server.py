'''
The initial genesis account that holds genesis balance
During ICO it sends balances according to the number of capchas 
that every node solved

After ICO it chills
'''


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
        for node in server.server_node.all_nodes:
            print(node)
    
    def ICO(self):
        for node in server.server_node.all_nodes:
            message = { 'id' : node.id, 'ICO' : 5 }
            self.server_node.send_to_nodes(message) 
            # self.server_node.send_to_nodes("ICO")
            print(f'sent ICO: {message}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_const', const=1, help='Test simple one-thread test')
    parser.add_argument('-n', action='store', help='Number of nodes to connect to perform ICO')
    args = parser.parse_args()

    # # Run simple test for blockchain
    # if args.test is not None:
    #     chain = bc.Blockchain()
    #     chain.append({"from": "John", "to": "Bob", "amount": 100})
    #     chain.append({"from": "bob", "to": "john", "amount": 50})
    #     print(chain)
    #     quit()

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
    # running = 1
    # while running:
    #     pass



    server.stop_server()
    # print(app)
    # app.run(debug=True)
