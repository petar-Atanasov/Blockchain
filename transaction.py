import random
random.seed(0)

def makeTransaction(maxValue = 3):
    
    # This will create valid transaction in the rnage of (1, maxValue)
    sign = int(random.getrandbits(1)) * 2 - 1 # Will randomly choose -1 or 1
    amount = random.randint(1, maxValue)
    alicePays = sign * amount
    bobPays = -1 * alicePays
    
    # By construction, this will always return transaction of tokens.
    # However, note that we have not done anything to check whether these overdraft an account
    
    return {u'Alice':alicePays, u'Bob':bobPays}

    txnBuffer = [makeTransaction() for i in range(30)]
    