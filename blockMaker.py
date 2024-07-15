from hashFun import hashMe

class BlockMaker:
    def makeBlock(self, txns, chain):
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

