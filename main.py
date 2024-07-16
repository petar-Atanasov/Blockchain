import sys

# from blockChecker import BlockCheker
from blockMaker import BlockMaker
from chainChecker import ChainCheker
from hashFun import hashMe
from transaction import Transaction
from stateUpdater import StateUpdater
from nodeSimulator import NodeSimulator


class Main:
    def __init__(self):
        self.state = {"Alice": 50, "Bob": 50}
        self.chain = self.createGenesisBlock()

    # NOTE - to delete if not needed
    # print(isValid({'Alice':-3, 'Bob':3},state))
    # print(isValid({'Alice':-4, 'Bob':3},state)) # cannot create or destroy tokens!
    # print(isValid({'Alice':-6, 'Bob':6},state)) # we also cannot overdraft out account.
    # print(isValid({'Alice':-4, 'Bob':2,'Lisa':2},state)) # creating new users is valid
    # print(isValid({'Alice':-4, 'Bob':3, 'Lisa':2},state)) # but the same rules still apply!

    def createGenesisBlock(self):
        # create the genesis block transaction and contents
        genesisBlockTxns = [self.state.copy()]  # copy yhe state
        genesisBlockContents = {
            "blockNumber": 0,
            "parentHash": None,
            "txnCount": 1,
            "txns": genesisBlockTxns,
        }
        # generate the hash for the genesis block with callback
        genesisHash = hashMe(genesisBlockContents)

        # assemble the genesis block
        genesisBlock = {
            "hash": genesisHash,
            "contents": genesisBlockContents
            }

        # NOTE - to delete if not needed
        # convert the genesis block to sorted JSON format
        # genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

        #!SECTION
        # print(genesisBlockStr)

        return [genesisBlock]

    def simulateTransactions(self, txnBuffer):
        blockSizeLimit = 5  # Arbitnary number of transaction per block

        # this is chosen by the blockm iner, and can vary between blocks!

        while txnBuffer:
            # Gather a set of valid trnsactions for inclusion
            txnList = []
            while txnBuffer and len(txnList) < blockSizeLimit:
                newTxn = txnBuffer.pop(0)
                validTxn = StateUpdater.isValid(
                    newTxn, self.state
                )  # returns false if txn is invalid

            if validTxn:  # if we got valid state, not false
                txnList.append(newTxn)
                self.state = StateUpdater.updateState(newTxn, self.state)
            else:
                print(f"ignored transaction {newTxn} due to validation failure.")
                sys.stdout.flush()

            ## Make a block
            if txnList:
                myBlock = BlockMaker.makeBlock(txnList, self.chain)
                self.chain.append(myBlock)

    def run(self):
        txnBuffer = Transaction.generateTransactionBuffer()
        self.simulateTransactions(txnBuffer)
        ChainCheker.checkChain(self.chain)
        self.simulateNode()
    
    def simulateNode(self):
        self.chain, self.state =  NodeSimulator.simulateNode(self.chain, self.state)  


if __name__ == "__main__":
    app = Main()
    app.run()
