
import os
import requests
from dotenv import load_dotenv
load_dotenv()
from mnemonic import Mnemonic
from bip44 import Wallet
from web3 import Account

import streamlit as st
from IPython.display import display

from web3.auto.infura.kovan import w3
#from web3 import middleware
#from web3.gas_strategies.time_based import medium_gas_price_strategy

def generate_account():
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""

    load_dotenv()

    # Fetch mnemonic from environment variable.
    mnemonic = os.getenv("MNEMONIC")

    if mnemonic is None:
        # If the mnemonic variable is none, initialize a new instance of Mnemonic
        # pass it a string value of english to use the english word list
        # Save the instance as a variable named mnemo
        mnemo = Mnemonic("english")
        # Call mnemo.generate(strength=256) and set it equal to the variable mnemonic 
        mnemonic = mnemo.generate(strength=256)

        #st.write("You do not have a mnemonic phrase yet. Here is one generated at random.")
        #st.write("Please add this to your environment file: ")
        #display(mnemonic)

        # CREATE ENV FILE ON THE FLY & SAVE MNEMONIC TO FILE ...

    # st.write("Please make sure the '.env' file has this value in it. Mnemonic: " + mnemonic)

    # Create Wallet Object
    wallet = Wallet(mnemonic)

    # Derive Ethereum Private Key
    private, public = wallet.derive_account("eth")

    # Convert private key into an Ethereum account
    account = Account.privateKeyToAccount(private)

    private_key = account.privateKey

    return mnemonic, private_key, account

def get_balance(address):
    
    # Access the balance of funds for the Ethereum account
    wei_balance = w3.eth.getBalance(address)

    # Convert the balance from a denomination in wei to ether
    ether = w3.fromWei(wei_balance, "ether")

    # return number of ether
    return ether, wei_balance
