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
        self.all_blockchains = {}

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

    def get_balance(self):
        return int(self.blockchain[-1].data['balance'])

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
        print("node_message (" + self.id + ") from " + node.id + ": " + str(message))

        if self.check_message(message):
            if ('type' in message):
                if (message['type'] == 'discovery'):
                    self.recieve_discovery(node, message)
                elif (message['type'] == 'discovery_answer'):
                    self.receive_discovery_answer(node, message)
                elif (message['type'] == 'ICO'):
                    self.perform_ICO(node, message)
                elif (message['type'] == 'ICO_request'):
                    self.recieve_ICO_req(node, message)

                elif (message['type'] == 'Send'):
                    self.recieve_send(node, message)
                elif (message['type'] == 'Recieve'):
                    self.recieve_recieve(node, message)
                else:
                    pass
    
    def check_message(self, message):
    # Checks if message is valid
        return True 

    def make_message(self, message):
    # Creates message that will be sent to other nodes
        if 'type' not in message:
            if 'data' in message['data']:
                message['type'] = message['data']['type']

        # if 'id' not in message:
        #     message['id'] = self.id
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
        data = {
                'type' : 'Recieve',
                'address' : message['id'],
                'signature' : node.id,
                'balance' : message['ICO'],
                'representative' : self.id,
            }
        
        if message['id'] == self.id:
            self.blockchain.append(data=data, timestamp = time.time())
            self.send_to_nodes(self.make_message({
                'type' : 'ICO_request',
                'data' : self.blockchain[-1].data,
                'nonce' : self.blockchain[-1].nonce,
                '_hash' : self.blockchain[-1]._hash,
                'prevHash' : self.blockchain[-1].prevHash,
                'timestamp' : self.blockchain[-1].timestamp
        }))

    def recieve_ICO_req(self, node, message):
        block = bc.Block(
                    data = message['data'],
                    nonce = message['nonce'],
                    _hash = message['_hash'],
                    prevHash = message['prevHash'],
                    timestamp = message['timestamp']
                )
        self.all_blockchains[message['data']['address']] = bc.Blockchain()
        self.all_blockchains[message['data']['address']].chain.append(block)




    def transaction_send(self, address, amount):
        data={
                'type' : 'Send',
                'link' : address,
                # 'previous' : self.blockchain[-1],
                'signature' : self.id,
                'balance' : self.get_balance() - int(amount),
                'representative' : self.id,
                'amount' : amount # BAD SHOULD CALCULATE IT BY BLOCK[-2] - BLOCK[-1]
            }

        self.blockchain.append(data=data, timestamp = time.time())
        self.send_to_nodes(self.make_message({
            'type' : 'Send',
            'data' : self.blockchain[-1].data,
            'nonce' : self.blockchain[-1].nonce,
            '_hash' : self.blockchain[-1]._hash,
            'prevHash' : self.blockchain[-1].prevHash,
            'timestamp' : self.blockchain[-1].timestamp
        }))




    def recieve_send(self, node, message):        
        if message['data']['link'] == self.id:
            data = {
                'type' : 'Recieve',
                'link' : message['data']['signature'],
                # 'previous' : self.blockchain[-1],
                'signature' : self.id,
                'balance' : self.get_balance() + int(message['data']['amount']),
                'representative' : self.id,
                'amount' : message['data']['amount']
            }
            self.blockchain.append(data=data, timestamp = time.time())
            self.send_to_nodes(self.make_message({
                'type' : 'Recieve',
                'data' : self.blockchain[-1].data,
                'nonce' : self.blockchain[-1].nonce,
                '_hash' : self.blockchain[-1]._hash,
                'prevHash' : self.blockchain[-1].prevHash,
                'timestamp' : self.blockchain[-1].timestamp
            }))
        else:
            if self.ValidSend(node, message):
                block = bc.Block(
                    data = message['data'],
                    nonce = message['nonce'],
                    _hash = message['_hash'],
                    prevHash = message['prevHash'],
                    timestamp = message['timestamp']
                )
                print('appending all_blockchains')
                self.all_blockchains[message['data']['signature']].chain.append(block)
            else:
                print(f'{bcolors.FAIL}Someone is trying to ruin BC!{bcolors.ENDC}')



    def recieve_recieve(self, node, message):
        if message['data']['link'] == self.id:
            if self.ValidRecieve(node, message): # check if we had sent to this address
                block = bc.Block(
                        data = message['data'],
                        nonce = message['nonce'],
                        _hash = message['_hash'],
                        prevHash = message['prevHash'],
                        timestamp = message['timestamp']
                    )
                self.all_blockchains[message['data']['signature']].chain.append(block)
            else:
                print(f'{bcolors.FAIL}Someone is trying to ruin BC by recieve!{bcolors.ENDC}')
            # otherwise dont validate!!!!
            pass
        else:
            if self.ValidRecieve(node, message):
                block = bc.Block(
                    data = message['data'],
                    nonce = message['nonce'],
                    _hash = message['_hash'],
                    prevHash = message['prevHash'],
                    timestamp = message['timestamp']
                )
                print('appending all_blockchains')
                self.all_blockchains[message['data']['signature']].chain.append(block)
            else:
                print(f'{bcolors.FAIL}Someone is trying to ruin BC by send!{bcolors.ENDC}')
    

    def ValidSend(self, node, message):
        block = bc.Block(
            data = message['data'],
            nonce = message['nonce'],
            _hash = message['_hash'],
            prevHash = message['prevHash'],
            timestamp = message['timestamp']
        )
        print('appending all_blockchains')
        self.all_blockchains[message['data']['signature']].chain.append(block)
        if self.all_blockchains[message['data']['signature']].isValid():
            self.all_blockchains[message['data']['signature']].chain.pop()
            return True
        else:
            self.all_blockchains[message['data']['signature']].chain.pop()
            return False

    def ValidRecieve(self, node, message):
        block = bc.Block(
            data = message['data'],
            nonce = message['nonce'],
            _hash = message['_hash'],
            prevHash = message['prevHash'],
            timestamp = message['timestamp']
        )
        print('appending all_blockchains')
        self.all_blockchains[message['data']['signature']].chain.append(block)
        if self.all_blockchains[message['data']['signature']].isValid():
            self.all_blockchains[message['data']['signature']].chain.pop()
            return True
        else:
            self.all_blockchains[message['data']['signature']].chain.pop()
            return False



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

        # with open (f"data_keys\{self.port}private.pem", "w+") as prv_file:
        #     print("{}".format(private_key.exportKey()), file=prv_file)

        # with open (f"data_keys\{self.port}public.openssh", "w+") as pub_file:
        #     print("{}".format(public_key.exportKey(format='OpenSSH')), file=pub_file)   



        return 1, self.port
 
    def get_public_key(self):
        return 1