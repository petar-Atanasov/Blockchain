import random
random.seed(0)

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