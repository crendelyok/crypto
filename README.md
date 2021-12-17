# Crypto
## Description
Model of cryptocurrnecy based on nano crypto. 
Blockchain based block-lattice structure etc.

>https://docs.nano.org/whitepaper/english/

Unfortunately, net must me fully-connected. For our purposes it is easier: we don`t need to broadcast every message. Full-connected net ensures that every node will recieve every message directly from the sending node. 
**Bad solution: we cannot scale the net.**
## Installation
>pip install pycryptodome \
pip install p2pnetwork \
pip install argon2-cffi

## How to run
### Step 1 
>python ./server

Runs server. Nodes have 30s to connect to the server to participate in ICO. Every node gets a reward of 5 coins during ICO. After ICO, server still works. It recieves all transactions and fills ledger.  

### Step 2
>python ./node -p [port] -i [optional --ico]

-p [port] (int) port of the node. It must be unique across one host ip.

-i [optional --ico] (It`s a flag) If node wants to participate in ICO.
 
Runs node. 'Port' is also acting like an 'id'. 

[TO DO] Ideally, 'id' aka 'signature' of each node is generated using crypto alghoritms.

### Step 3

Steps 1 and 2 are not protected. Step 3 is protected. From now on, nodes use **PoS, block-lattice structures, hashes and signatures**, so they are immune to different types of attacks.

### We can type commands to the running terminal.

Server commands:

1) ['s'] stop server 
2) ['show'] show ledger

Node commands:

1) ['s'] stop server 
2) ['show'] show ledger
3) ['balance'] show local blockchain
4) ['send'] send money to someone
5) and more

## TO DO
1) PoS (or ORV Consensus).
2) Signatures aka ids.
3) Get rid off fully-connected net.
4) Get rid of messy code lmao. Including wrapping data and messages into usable class.
5) 'Cementing' blocks in local blockchain.
6) New type of blocks: 'Changing representative'.
7) Make tests to imitate different attacks (like double spend,  51%, DDOS, Precomputed POW attack etc. (check nano docs))
8) Didn`t test WITHOUT ICO.