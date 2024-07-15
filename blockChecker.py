from hashFun import hashMe
import copy 

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
    
    # parentNumber = parent['contents']['blockNumber']
    # parentHash = parent['hash']
    # blockNumber = block['contents']['blockNumber']
    
    # Check transaction validity:
    # throw and error if an invalid transaction was found 
   # print(f"Before transaction: {state}")
    #print(f"Current state before processing clock {block['contents']['blockNumber']}: {state}")
        try:
            for txn in block['contents']['txns']:
            #print(f"Processing transaction {txn} with state {state}")
                if isValid(txn,state): # type: ignore
                    state = updateState(txn,state) # type: ignore
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
    
    @staticmethod
    def isValid(txn, state):
    # Assume that the transaction is a dictionary keyed by account names
    
    # Check that the sum of the deposit and withdrawls is -
    # print(f"Checking transaction {txn} with current state {state}")
        if sum(txn.values()) != 0:
            return False
    
    # Check that the transaction does not cause an overdraft
        for key, amount in txn.items():
            current_balance = state.get(key, 0)
            if current_balance + amount < 0:
                return False
        return True
    
    @staticmethod
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