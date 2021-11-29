
import streamlit as st                          # only needed for testing
import web3
from web3 import Web3
import json

# from dotenv import load_dotenv
# load_dotenv()
# import os
# import requests
# import streamlit as st
# from web3 import middleware
# from web3.gas_strategies.time_based import medium_gas_price_strategy
# from web3 import Account
# from web3.auto.infura.kovan import w3
# w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/d7336d8a44fc42a1a9a21662bf242bdb'))

# Infura Kovan Project ID: d7336d8a44fc42a1a9a21662bf242bdb
# Infura EndPoint for above Project ID: https://kovan.infura.io/v3/d7336d8a44fc42a1a9a21662bf242bdb

# Request eth from here
infura_url = "https://kovan.infura.io/v3/d7336d8a44fc42a1a9a21662bf242bdb"
web3_infura = Web3(Web3.HTTPProvider(infura_url))

# infura_url_main_net = "https://mainnet.infura.io/v3/d7336d8a44fc42a1a9a21662bf242bdb"
# web3_infura_url_main_net = Web3(Web3.HTTPProvider(infura_url_main_net))
# infura_project_id = "d7336d8a44fc42a1a9a21662bf242bdb"

# Transactions on ganache
ganache_url = "HTTP://127.0.0.1:7545"
web3_ganache = Web3(Web3.HTTPProvider(ganache_url))

# using for testing
metamask_account_03 = "0xf1F319e20746155195BC062db8b978969daD4B43"

def is_infura_connected():
    success = False
    if web3_infura.isConnected():
        st.success("web3 (infura) is connected")
        block = web3_infura.eth.blockNumber
        balance = web3_infura.eth.get_balance(metamask_account_03)
        ether = web3_infura.fromWei(balance, "ether")

        success = True
        return success, block, balance, ether
    else:
        return success, 0, 0, 0

# def token_info(contract_address):
#     abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"sender","type":"address"},{"name":"recipient","type":"address"},{"name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"value","type":"uint256"}],"name":"burn","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"recipient","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"name","type":"string"},{"name":"symbol","type":"string"},{"name":"decimals","type":"uint8"},{"name":"totalSupply","type":"uint256"},{"name":"feeReceiver","type":"address"},{"name":"tokenOwnerAddress","type":"address"}],"payable":true,"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"}]')
#     contract = web3_infura.eth.contract(address=contract_address, abi=abi)
#     print(contract)
#     # total_supply = web3_infura.eth.contract()
#     # #.contract(address=contract, abi=abi)
#     # st.info(contract)


def is_ganache_connected():
    success = False
    if web3_ganache.isConnected():
        st.success("web3 (ganache) is connected")
        block = web3_ganache.eth.blockNumber
        success = True
        return success, block
    else:
        return success, 0

def transaction_ganache(sender_account_ganache, sender_private_key, receiver_account_ganache):
    success = False
    web3_ganache = Web3(Web3.HTTPProvider(ganache_url))
    # Building Transaction for ganache 
    # st.warning(sender_account_ganache)
    # print(web3_ganache.eth.get_balance(sender_account_ganache))
    # st.warning(receiver_account_ganache)
    # print(web3_ganache.eth.get_balance(receiver_account_ganache))
    # get tyhe nonce
    nonce = web3_ganache.eth.get_transaction_count(sender_account_ganache)
    # # build the transaction json
    tx = {
        'nonce' : nonce,
        'to' : receiver_account_ganache,
        'value' : web3_ganache.toWei(1, 'ether'),
        'gas' : 2000000,
        'gasPrice' : web3_ganache.toWei('50', 'gwei')
    }
    # sign transaction
    signed_tx = web3_ganache.eth.account.signTransaction(tx, sender_private_key)
    # send transaction
    tx_hash = web3_ganache.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_hash_hex = web3_ganache.toHex(tx_hash)
    # get transaction hash
    if (tx_hash):
        success = True
        new_balance_sender = web3_ganache.fromWei(web3_ganache.eth.get_balance(sender_account_ganache), 'ether')
        new_balance_receiver = web3_ganache.fromWei(web3_ganache.eth.get_balance(receiver_account_ganache), 'ether')
        return success, tx_hash, tx_hash_hex, new_balance_sender, new_balance_receiver
    else:
        success = False
        return success, 0, 0, 0



# ==================================================
# # def is_wallet_installed():
#     # if window.ethereum{}
#     st.write("Testing ABCDEFG")
#     return 786