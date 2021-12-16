# Crypto
## Description
Model of cryptocurrnecy based on nano crypto. 
Blockchain based block-lattice structure etc.

Unfortunately, net must me fully-connected. It is easier: we don`t need to broadcast every message we get to all known nodes. 
It is a bad solution: we cannot scale the net.
## Installation
>pip install pycryptodome \
pip install p2pnetwork 

## How to run
### Step 1 
>python ./server

Runs server. Nodes have 30s to connect to the server to participate in ICO. Every node gets a reward of 5 coins during ICO.

### Step 2
>python ./node -p [port]

Make sure each port is unique for every node. Port is also acting like an id. This is the first assumption: 
each node has a unique id.

### Step 3

Steps 1 and 2 are not protected. Step 3 is protected. From now on, nodes use **PoS, block-lattice structures, hashes and signatures**, so they are immune to different types of attacks.



