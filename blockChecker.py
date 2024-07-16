import copy

from hashFun import hashMe 
from stateUpdater import StateUpdater

class BlockCheker:
    @staticmethod
       # helper function that makes sure that the block contents match the hash
    def checkBlockHash(block):
    # raise an exception if the hash does not match the block
        expectedHash = hashMe(block['contents'])
    
        if block['hash'] != expectedHash:
            raise Exception(f'Hash does not match the contents of the cloack block  {block["contents"]["blockNumber"]}')

#Checks the validity of a block,
# return the updated state if the block is valid, and raise an error otherwise.
    @staticmethod
    def checkBlockValidity(block, parent, state):
    
    # backup the state 
        original_state = copy.deepcopy(state)
   
    #We want to check the following:
    # 1. Each of the transactions are valid updates to the system state
    # 2. Block hash is valid for the block contents
    # 3. Block number increments the parent block number by 1
    # 4. Accurately references the parent block's hash
    
    # Check transaction validity:
    # throw and error if an invalid transaction was found 
   # print(f"Before transaction: {state}")
    #print(f"Current state before processing clock {block['contents']['blockNumber']}: {state}")
        try:
            for txn in block['contents']['txns']:
            #print(f"Processing transaction {txn} with state {state}")
                if StateUpdater.isValid(txn,state): # type: ignore
                    state = StateUpdater.updateState(txn,state) # type: ignore
                #print(f"After transaction {txn}: , the state is {state}")
                else:
                    raise Exception(f'Invalid transaction in the block {block["contents"]["blockNumber"]}: {txn}') 
        
        # checkBlockHash(block) # check the hash integrity, raises an error if inaccurate
    
            if block['contents']['blockNumber'] != parent['contents']['blockNumber'] + 1:
                raise Exception(f'Block number does not increment correctly from {parent["contents"]["blockNumber"]} to {block["contents"]["blockNumber"]}')
        
            if block['contents']['parentHash'] != parent['hash']:
                raise Exception(f'Parent hash not accurate at block {block["contents"]["blockNumber"]}')
    
        except Exception as e:
        #revert back the state
            state = original_state
            raise e
    
        return state    