
import streamlit as st
from IPython.display import display
from dataclasses import dataclass
#from datetime import datetime
import datetime as datetime
from typing import Any, List
import pandas as pd
import hashlib

from sr_functions import *

################################################################################
# Saeed Raghib
# Step 1:
# Create a Record Data Class

# Define a new Python data class named `Record`. Give this new class a
# formalized data structure that consists of the `sender`, `receiver`, and
# `amount` attributes. To do so, complete the following steps:
# 1. Define a new class named `Record`.
# 2. Add the `@dataclass` decorator immediately before the `Record` class
# definition.
# 3. Add an attribute named `sender` of type `str`.
# 4. Add an attribute named `receiver` of type `str`.
# 5. Add an attribute named `amount` of type `float`.
# Note that you’ll use this new `Record` class as the data type of your `record` attribute in the next section.

# Create a Record Data Class that consists of the `sender`, `receiver`, and
# `amount` attributes
# YOUR CODE HERE
@dataclass
class Record:
    sender: str
    receiver: str
    amount: float
    file_PK: str        # THIS IS HOW WE WILL KNOW TO ACCESS THE FILE IMAGE TO DISPLAY???

################################################################################
# Step 2:
# Modify the Existing Block Data Class to Store Record Data

# Rename the `data` attribute in your `Block` class to `record`, and then set
# it to use an instance of the new `Record` class that you created in the
# previous section. To do so, complete the following steps:
# 1. In the `Block` class, rename the `data` attribute to `record`.
# 2. Set the data type of the `record` attribute to `Record`.

@dataclass
class Block:

    # @TODO
    # Rename the `data` attribute to `record`, and set the data type to `Record`
    # data: Any
    record: Record

    creator_id: int     # SHOULD BE STRING ... ?????
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()


@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

# Testing the side bar. 
# Maybe use for title. If not can be commented later
st.sidebar.markdown("# TAX WARRIORS")
st.sidebar.markdown("# Its ALIVE!!!!!")

##############################      SIGN UP     ################

# The FINAL code will rad this from either the 'sign up' or 'log in' workflow. 
first_name = "Saeed"
last_name = "Raghib"
email = "saeed_raghib@msn.com"
cell_number = "2143344726"

# Signup Process
#   Gather Data
#       KYC:
#           First Name, Last Name, email, sell phone
#   Generate Account
#       Create Mnemonic
#       Create Wallet
#       Buy Eth ... use INFURA
#       Create Genesis Block

# CREATE & GET ACCOUNT & WALLET
result = generate_account()
#st.write("Please make sure the '.env' file has this value in it for nexttime use. Mnemonic: ")
display(result[0])
st.write("Private Key is: ")
st.write(result[1])
address = result[2].address
st.write("Wallet Address: " + address)


# GET BALANCE IN ETHER & WEI
balance = get_balance(address)
balance_ether = balance[0]
balance_wei = balance[1]
#display(balance)
#print(balance)
st.write("Wallet Balance (in ethereum): " + str(balance_ether))
st.write("Wallet Balance (in wei): " + str(balance_wei))

# CREATE GENESIS BLOCK
# Streamlit Code

# Adds the cache decorator for Streamlit

@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])

st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

##############################      LOG IN     ################

# 1.00:     FIND RECEIPT ON YOUR HARD DRIVE
# 1.01:     UPLOAD RECEIPT
# 2.00:     ADD TO DATABASE
# 2.05:     GET PRIMARY KEY
# 2.10:     ADD TO RECORD
# 2.15:     CREATE BLOCK HASH
# 2.18:     DATABASE SCHEMA:
#		        Primary Key: 	generated by database
#		        PK_Hash:		generated by code
#		        first_name:		KYC
#		        last_name:		KYC
#		        email:			KYC
#		        cell_number:	KYC
#		        Block Hash		generated by code.
#           						added to db
#						            used to refer to image file		<-- 	This is the answer to saving the and retrieving the block chain for any customer!!!
#		        image file:		image of receipt ...                
# 2.20:     ADD BLOCK HASH TO DATABASE
# 3.00:     ABILITY TO NAVIGATE ALL RECEIPTS - HOW WILL THIS WORK???
