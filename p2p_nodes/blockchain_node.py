from p2pnetwork.node import Node
import p2p_nodes.blockchain.blockchain as bc
import time
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import argon2, binascii

from configuration import *

class BlockchainNode (Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(BlockchainNode, self).__init__(host, port, id, callback, max_connections)
        self.debug = False
        self.connection_debug = True

        self.blockchain = bc.Blockchain()

        self.discovery_messages = {}
        self.known_ids = []
        # Account
        self.key = self.key_pair_generate() # public key, private is stored in memory
        self.id = repr(self.key[1]) # the public key



    #######################################################
    # Useful methods                                      #
    #######################################################

    def print_known_ids(self):
        print(f'Known ids for node id {self.id}')
        for known_id in self.known_ids:
            print(known_id)
        print('\n')

    def print_connection_debug(self, data):
        if self.connection_debug:
            print(data)

    #######################################################
    # Connect and disconnect                              #
    #######################################################

    def outbound_node_connected(self, node):
        if node.id not in self.known_ids:
            self.known_ids.append(node.id)
        self.print_connection_debug("outbound_node_connected (" + self.id + "): " + node.id)
        
    def inbound_node_connected(self, node):
        if node.id not in self.known_ids:
            self.known_ids.append(node.id)
        self.print_connection_debug("inbound_node_connected: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        self.print_connection_debug("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        self.print_connection_debug("outbound_node_disconnected: (" + self.id + "): " + node.id)
        
    def node_disconnect_with_outbound_node(self, node):
        self.print_connection_debug("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        self.print_connection_debug("node is requested to stop (" + self.id + "): ")


    #######################################################
    # Getting and sending messages                        #
    #######################################################

    def node_message(self, node, message):
    # When 'this node' gets 'message' from 'node'
        # print("node_message (" + self.id + ") from " + node.id + ": " + str(message))

        if self.check_message(message):
            if ('type' in message):
                if (message['type'] == 'discovery'):
                    self.recieve_discovery(node, message)
                elif (message['type'] == 'discovery_answer'):
                    self.receive_discovery_answer(node, message)
                elif (message['type'] == 'ICO'):
                    self.perform_ICO(node, message)
                else:
                    pass
    
    def check_message(self, message):
    # Checks if message is valid
        return True 

    def make_message(self, message):
    # Creates message that will be sent to other nodes
        if 'id' not in message:
            message['id'] = self.id

        # message['timestamp'] = time.time()
        # message['hash'] = self.get_hash(message)
        # message['sign'] = self.get_sign()
        # message['public_key'] = self.get_public_key()
        return message

    def send_message(self, message):
    # Broadcast mesasge to nodes
        self.send_to_nodes(self.make_message(message))

    #######################################################
    # Dicovery messages recieve and answer. Network logic #
    #######################################################
    
    def send_discovery(self):
    # Self discovery to all connected nodes
        self.send_to_nodes(self.make_message(
            {'type' : 'discovery', 'ip' : self.host, 'port' : self.port, 'id' : self.id}
        ))

    def recieve_discovery(self, node, message):
    # Deal with 'dicovery' type of message
        if message['id'] not in self.known_ids and message['id'] != self.id:
            self.known_ids.append(message['id'])

        if message['id'] in self.discovery_messages:
        # already discovered so no need to deal with it
            pass 
        else:
            self.send_to_nodes(message, [node]) #relay
            self.discovery_messages[message['id']] = message

            # then, if not connected we connect
            connected = False
            for n in self.all_nodes:
                if n.id == message['id'] or self.id == message['id']:
                    connected = True
            if not connected:
                self.connect_with_node(message['ip'], message['port'])


    #######################################################
    # Transcations(send, recieve) and ICO                 #
    #######################################################

    def perform_ICO(self, node, message):
    # Saving ICO. Not protected. 
    # It creates first non-genesis block
    # And add it to local blockchain
        if message['id'] != self.id:
            return

        self.blockchain.append(data=
            {
                'type' : 'Recieve',
                'address' : self.id,
                'previous' : 0,
                'from' : node.id,
                'balance' : message['ICO'],
                'representative' : self.id,

            }, timestamp = time.time()
        )

        print(self.blockchain)


    #######################################################
    # Cryptography. Hashing, signing etc.                 #
    #######################################################

    def get_hash(self, message):
    # Hashes the message and returns it
        return 1
    
    def get_sign(self):
    # Returns sign of the node
        return 1
    
    def encrypt(self):
        publickey = self.key.publickey() # pub key export for exchange
        encrypted = publickey.encrypt('encrypt this message', 32)
        print ('encrypted message:', encrypted)
        f = open ('encryption.txt', 'w+')
        f.write(str(encrypted)) #write ciphertext to file
        f.close()

        return encrypted

    def decrypt(self, data):
        f = open('encryption.txt', 'r')
        message = f.read()
        # преобразовать ключ из str в кортеж перед расшифровкой
        decrypted = self.key.decrypt(ast.literal_eval(str(data)))
        print ('decrypted', decrypted)
        f = open ('encryption.txt', 'w')
        f.write(str(message))
        f.write(str(decrypted))
        f.close()

    def key_pair_generate(self):
    # Returns tuple (private, public)
        # key = RSA.generate(2048)
        # # Should save to use them in case the node`s power off 
        # print(f'{bcolors.OKGREEN}{key}{bcolors.ENDC}')
        # print(f'{bcolors.OKGREEN}{key.public_key()}{bcolors.ENDC}')
        # return (1, self.port)
        random_generator = Random.new().read
        private_key = RSA.generate(1024, random_generator)
        public_key = private_key.publickey()
        # print(private_key.exportKey(format='PEM'))
        # print(public_key.exportKey(format='OpenSSH'))

        with open (f"data_keys\{self.port}private.pem", "w+") as prv_file:
            print("{}".format(private_key.exportKey()), file=prv_file)

        with open (f"data_keys\{self.port}public.openssh", "w+") as pub_file:
            print("{}".format(public_key.exportKey(format='OpenSSH')), file=pub_file)   



        return 1, 1
 
    def get_public_key(self):
        return 1