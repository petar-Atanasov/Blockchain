import json
import random
import copy
import sys
random.seed(0)
from hashFun import hashMe

def makeTransaction(maxValue = 3):
    
    # This will create valid transaction in the rnage of (1, maxValue)
    sign = random.choice([-1, 1]) # Will randomly choose -1 or 1
    amount = random.randint(1, maxValue)
    alicePays = sign * amount
    bobPays = -alicePays
    
    # By construction, this will always return transaction of tokens.
    # However, note that we have not done anything to check whether these overdraft an account
    
    return {'Alice': alicePays, 'Bob': bobPays}

txnBuffer = [makeTransaction() for i in range(30)]

state = {'Alice':5, 'Bob':5}

# print(isValid({'Alice':-3, 'Bob':3},state)) 
# print(isValid({'Alice':-4, 'Bob':3},state)) # cannot create or destroy tokens!
# print(isValid({'Alice':-6, 'Bob':6},state)) # we also cannot overdraft out account.
# print(isValid({'Alice':-4, 'Bob':2,'Lisa':2},state)) # creating new users is valid
# print(isValid({'Alice':-4, 'Bob':3, 'Lisa':2},state)) # but the same rules still apply!

state = {'Alice': 50, 'Bob': 50} # define the initial state

# create the genesis block transaction and contents
genesisBlockTxns = [state.copy()] # copy yhe state 
genesisBlockContents = {
    'blockNumber': 0,
    'parentHash': None,
    'txnCount': 1,
    'txns': genesisBlockTxns
    }
# generate the hash for the genesis block with callback
genesisHash = hashMe(genesisBlockContents)

#assemble the genesis block
genesisBlock = {
    'hash': genesisHash,
    'contents': genesisBlockContents
    }

# convert the genesis block to sorted JSON format
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

#!SECTION
# print(genesisBlockStr)

chain = [genesisBlock]

#sumilate transaction buffer 
txnBuffer = [
    {'Alice': -3, 'Bob': 3},
    {'Alice': -4, 'Bob': 4},
    {'Alice': -1, 'Bob': 1}
    ] * 10

blockSizeLimit = 5 # Arbitnary number of transaction per block
# this is chosen by the blockm iner, and can vary between blocks!

while txnBuffer:
    # Gather a set of valid trnsactions for inclusion
    txnList = []
    while txnBuffer and len(txnList) < blockSizeLimit:
        newTxn = txnBuffer.pop(0)
        validTxn = isValid(newTxn, state) # returns false if txn is invalid
        
        if validTxn: #if we got valid state, not false
            txnList.append(newTxn)
            state = updateState(newTxn,state)
        else:
            #print(f"ignored transaction {newTxn} due to validation failure.") 
            sys.stdout.flush()
    
    
    ## Make a block    
    if txnList:
        myBlock = makeBlock(txnList, chain)    
        chain.append(myBlock)

checkChain(chain)           

chainAsText = json.dumps(chain,sort_keys=True)
checkChain(chainAsText)
print((str)(chainAsText))


##!SECTION
#Blockchain Architechure 
