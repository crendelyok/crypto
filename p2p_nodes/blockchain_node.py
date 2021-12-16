from p2pnetwork.node import Node
import p2p_nodes.blockchain.blockchain as bc
import time

class BlockchainNode (Node):

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(BlockchainNode, self).__init__(host, port, id, callback, max_connections)
        self.blockchain = bc.Blockchain()
        self.rsa = None # make public and private keys
        self.discovery_messages = {} # aka known nodes

    #######################################################
    # Connect and disconnect                              #
    #######################################################

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")


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
                   
                else:
                    pass
    
    def check_message(self, message):
    # Checks if message is valid
        return True 

    def make_message(self, message):
    # Creates message that will be sent to other nodes
        message['id'] = self.id
        message['timestamp'] = time.time()
        message['hash'] = self.get_hash(message)
        message['sign'] = self.get_sign()
        message['public_key'] = self.get_public_key()
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
            {'type' : 'discovery', 'id' : self.id, 'timestamp' : time.time()}
        ))

    def recieve_discovery(self, node, message):
    # Deal with 'dicovery' type of message
        if message['id'] in self.discovery_messages:
            # already discovered so no need to deal with it
            pass 
        else:
            self.discovery_messages[message['id']] = node
            self.send_discovery_answer(node, message)
            self.send_to_nodes(self.make_message({}))

    def send_discovery_answer(self, node, message):
    # Send discovery answer after getting discovery message
    # Answer contains all nodes that we are connected to
        nodes = []
        for n in self.nodes_inbound:
            nodes.append({'id': n.id, 'ip': n.host, 'port': n.main_node.port, 'connection': 'inbound'})
        for n in self.nodes_outbound:
            nodes.append({'id': n.id, 'ip': n.host, 'port': n.port, 'connection': 'outbound'})

        node.send(self.make_message(
            {'id': message['id'], 'type': 'discovery_answer', 'timestamp': message['timestamp'], 'nodes': nodes}
            ))
             
    def receive_discovery_answer(self, node, message):
    # Send answer to discovery_answer
        if message['id'] in self.discovery_messages:
            self.send_discovery_answer(self.discovery_messages[message['id']], message)

        else:
            if (message['id'] == self.id):
                # I was waiting for this!
                pass
            else:
                # Something strange!
                pass


    #######################################################
    # Cryptography. Hashing, signing etc.                 #
    #######################################################

    def get_hash(self, message):
    # Hashes the message and returns it
        return 1
    
    def get_sign(self):
    # Returns sign of the node
        return 1
    
    def get_public_key(self):
    # Returns public key of the node   
        return 1
