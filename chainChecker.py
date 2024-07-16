import json

from blockChecker import BlockCheker
from stateUpdater import StateUpdater

class ChainCheker:
    @staticmethod
    def checkChain(chain):
    #!SECTION
    # Work through the chain from the genesis block (which gets spectial treatment),
    # checking that all thransactions are internally valid,
    # that the transcation do not cause an overdraft,
    # and that the block are linked by their hashes.
    
    #NOTE
    # This returns the state as a dictionary of accounts and balances,
    # or returns false if an error was detected
    
    ##NOTE - Data input processing:
    # make sure that our chain is a list of dicts
        if isinstance(chain, str):
            try:
                chain = json.loads(chain)
                assert isinstance(chain, list)
            except: #This is a catch-all admittedly crude
                return False
        elif not isinstance(chain, list):
            return False
    
        state = {'Alice': 50, 'Bob': 50}
    ##!SECTION Prime the pump by checking the genesis block
    # We want to check the following:
    # 1. Each of the transactions are valid updates to the system state
    # 2. Block hash is valid for the block contents
    
        for txn in chain[0]['contents']['txns']:
            state = StateUpdater.updateState(txn,state)
        BlockCheker.checkBlockHash(chain[0])
        parent = chain[0]
    
    ##!SECTION Checking subsequent blocks:
    # These additionally need to check
        # the reference to the parent block's hash
        # the validity of the block number
        
        for block in chain[1:]:
        #print(f"Validating block {block['contents']['blockNumber']} with parent block {parent['contents']['blockNumber']}")
            state = BlockCheker.checkBlockValidity(block, parent, state)
            parent = block
        
        return state