class StateUpdater:
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