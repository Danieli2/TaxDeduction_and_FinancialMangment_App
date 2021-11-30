import os
from dotenv import load_dotenv
load_dotenv()
from bip44 import Wallet
from web3 import Account
from web3.auto.infura.kovan import w3

# Access the balance of funds for the Ethereum account
wei_balance = w3.eth.getBalance(0xb0648be5d9fCDCb972570cB103BcD525DB44e2f1)

# Convert the balance from a denomination in wei to ether
ether = w3.fromWei(wei_balance, "ether")

# Print the number of ether
ether



# Access the balance of funds for the Ethereum account
wei_balance = w3.eth.getBalance(0xb0648be5d9fCDCb972570cB103BcD525DB44e2f1)

# Convert the balance from a denomination in wei to ether
ether = w3.fromWei(wei_balance, "ether")

# Print the number of ether
ether