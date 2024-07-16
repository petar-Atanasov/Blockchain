import random

random.seed(0)

class Transaction:
    @staticmethod
    def makeTransaction(maxValue = 3):
    
    # This will create valid transaction in the rnage of (1, maxValue)
        sign = random.choice([-1, 1]) # Will randomly choose -1 or 1
        amount = random.randint(1, maxValue)
        alicePays = sign * amount
        bobPays = -alicePays
    
    # By construction, this will always return transaction of tokens.
    # However, note that we have not done anything to check whether these overdraft an account
    
        return {'Alice': alicePays, 'Bob': bobPays}

    def generateTransactionBuffer(size = 30, maxValue = 3):
        return [Transaction.makeTransaction(maxValue) for _ in range(size)]