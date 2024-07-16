#!SECTION
#Blockchain Architechure 

import copy

from transaction import Transaction
from blockChecker import BlockCheker
from blockMaker import BlockMaker

class NodeSimulator:
    @staticmethod        
    def simulateNode(chain,state):
        print("Simulating node..")
        
        nodeBchain = copy.copy(chain)
        nodeBtxns = [Transaction.makeTransaction() for i in range(5)]
        newBlock = BlockMaker.makeBlock(nodeBtxns, nodeBchain)
        
        print("Blockchain on Node A is currently %s block long" % len(chain))
        
        try:
            print("New Block Reveived: Checking validity...")
            
            state = BlockCheker.checkBlockValidity(newBlock, chain[-1], state)
            
            ##SECTION -  Update the state
            #this will throw an error if the block is invalid!
            
            chain.append(newBlock)
        except Exception as e:
            print("Invalid block: Ignoring and waiting for the next block...")
            print(e)
        
        print("BlockChain on Node A is now %s blocks long"% len(chain))
        return chain,state        
                
