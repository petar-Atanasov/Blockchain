import hashlib
import json
import random
import sys
random.seed(0)
from hashFun import hashMe

def makeTransaction(maxValue = 3):
    
    # This will create valid transaction in the rnage of (1, maxValue)
    sign = int(random.getrandbits(1)) * 2 - 1 # Will randomly choose -1 or 1
    amount = random.randint(1, maxValue)
    alicePays = sign * amount
    bobPays = -alicePays
    
    # By construction, this will always return transaction of tokens.
    # However, note that we have not done anything to check whether these overdraft an account
    
    return {'Alice':alicePays, 'Bob':bobPays}

txnBuffer = [makeTransaction() for i in range(30)]

def updateState(txn, state):
    # Inputs: txn, state: dictinaries keyed with account names,
    # holding numeric values for transfer amount (txn) or account
    # balance (state)
        
    # Returns: Update state, with additional user added to state if necessary
    # NOTE: This does not validate the transaction - just updates the state!
        
    # If the transaction is valid, then update the state
    state = state.copy() # As dictionaries are mutable,
    # let's avoid any confusion by creating a working
    # copy of the data.
    for key in txn:
        if key in state.keys():
            state[key] = state.get(key, 0) + txn[key]
    return state 
    
           
def isValid(txn,state):
    # Assume that the transaction is a dictionary keyed by account names
    
    # Check that the sum of the deposit and withdrawls is -
    if sum(txn.values()) != 0:
        return False
    
    # Check that the transaction does not cause an overdraft
    for key, amount in txn.items():
        if state.get(key, 0) + amount < 0:
            return False
    return True

state = {'Alice':5, 'Bob':5}

print(isValid({'Alice':-3, 'Bob':3},state)) 
print(isValid({'Alice':-4, 'Bob':3},state)) # cannot create or destroy tokens!
print(isValid({'Alice':-6, 'Bob':6},state)) # we also cannot overdraft out account.
print(isValid({'Alice':-4, 'Bob':2,'Lisa':2},state)) # creating new users is valid
print(isValid({'Alice':-4, 'Bob':3, 'Lisa':2},state)) # but the same rules still apply!

state = {'Alice':50, 'Bob':50} # define the initial state

# create the genesis block transaction and contents
genesisBlockTxns = [state]
genesisBlockContents = {
    'blockNumber':0,
    'parentHash':None,
    'txnCount':1,
    'txns':genesisBlockTxns
    }
# generate the hash for the genesis block with callback
genesisHash = hashMe(genesisBlockContents)

#assemble the genesis block
genesisBlock = {
    'hash': genesisHash,
    'contents':genesisBlockContents
    }

# convert the genesis block to sorted JSON format
genesisBlockStr = json.dumps(genesisBlock,sort_keys=True)

#!SECTION
# print(genesisBlockStr)

chain = [genesisBlock]

def makeBlock(txns, chain):
    parentBlock = chain[-1]
    parentHash = parentBlock['hash']
    blockNumber = parentBlock['contents']['blockNumber'] + 1
    blockContents = {
        'blockNumber': blockNumber,
        'parentHash': parentHash,
        'txnCount': len(txns),
        'txns': txns
         }
    blockHash = hashMe(blockContents)
    block = {
        'hash': blockHash,
        'contents': blockContents
    }
    
    return block
#sumilate transaction buffer 
txnBuffer = [{'Alice': -3, 'Bob': 3}, {'Alice': 4, 'Bob': 4}, {'Alice': -1, 'Bob': 1}] * 10

blockSizeLimit = 5 # Arbitnary number of transaction per block
# this is chosen by the blockm iner, and can vary between blocks!

while txnBuffer:
    # Gather a set of valid trnsactions for inclusion
    txnList = []
    while txnBuffer and len(txnList) < blockSizeLimit:
        newTxn = txnBuffer.pop()
        validTxn = isValid(newTxn, state) # returns false if txn is invalid
        
        if validTxn: #if we got valid state, not false
            txnList.append(newTxn)
            state = updateState(newTxn,state)
        else:
            print("ignored transaction")
            sys.stdout.flush()    
            
    
    
    ## Make a block    
    if txnList:
        myBlock = makeBlock(txnList,chain)    
        chain.append(myBlock)
    
   #!SECTION
   # print("The number is ", state)
   
   # helper function that makes sure that the block contents match the hash
def checkBlockHash(block):
    # raise an exception if the hash does not match the block
    expectedHash = hashMe(block['contents'])
    
    if block['hash'] != expectedHash:
        raise Exception('Hash does not match the contents of the cloack %s' % block['contents']['blockNumber'])
    return

#Checks the validity of a block,
# return the updated state if the block is valid, and raise an error otherwise.

def checkBlockValidity(block, parent, state):
    #We want to check the following:
    # 1. Each of the transactions are valid updates to the system state
    # 2. Block hash is valid for the block contents
    # 3. Block number increments the parent block number by 1
    # 4. Accurately references the parent block's hash
    parentNumber = parent['contents']['blockNumber']
    parentHash = parent['hash']
    blockNumber = block['contents']['blockNumber']
    
    # Check transaction validity:
    # throw and error if an invalid transaction was found 
    for txn in block['contents']['txns']:
        if isValid(txn,state):
            state = updateState(txn,state)
        else:
            raise Exception('Invalid transaction in the block %s: %s' % (blockNumber, txn))    