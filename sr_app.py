import streamlit as st
import time
                                    # only needed for samples
# from web3 import Web3
from sr_functions import *
# import web3

def main():
    """ LogIn & SignUp: Check for Wallet & Connect """

# Transactions on ganache
ganache_url = "HTTP://127.0.0.1:7545"
web3_ganache = Web3(Web3.HTTPProvider(ganache_url))

# 9th account in local ganache blockchain
sender_account_ganache_09 = web3_ganache.eth.accounts[8]    # "0x2c259F120eB0312A2Ccb500cc894a215aA8d48B4"
sender_private_key_09 = "e1a32611987f64e3e40976f988fd0e723e4be97190b2b6ff7dd46a0050b0da33"      # How do I read the key
# 10th account in local ganache blockchain
receiver_account_ganache_10 = web3_ganache.eth.accounts[9]  # "0xeECa8e62924F1F596810Fa8ef2F4813B72ca6c68"

st.title("Login Workflow ONLY")

menu = ["Welcome", "Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Welcome":
    st.subheader("Welcome To **_WriteOff_ Warrior** app")
    comment = '<p style="font-family:Sans; color:Red; font-size: 20px;">If you haven\'t already, please install the MetaMask wallet. You will need it for this application</p>'
    st.write(comment, unsafe_allow_html=True)

    # Example: Is Infura Connected? - **************************
    result_infura = is_infura_connected()
    if result_infura[0]:       # i.e. success = True
        st.info("Latest Block: " + str(result_infura[1]))
        st.info("Balance in WEI: " + str(result_infura[2]))
        st.info("ether: " + str(result_infura[3]))
        st.balloons()
    else:
        st.error("Infura is not connected")
    time.sleep(1)

    # # Example: Reading A Contract (Shib Inu) - **************************
    # contract_address = "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce"
    # token_info(contract_address)
    # # wallet_exists = is_wallet_installed()
    # # print("The value returned is: " + str(wallet_exists))
    # # result = is_infura_connected()
    # # if result[0]:       # i.e. success = True
    # #     st.info("Latest Block: " + str(result[1]))
    # #     st.info("Balance in WEI: " + str(result[2]))
    # #     st.info("ether: " + str(result[3]))
    # #     st.balloons()
    # # else:
    # #     st.error("Infura is not connected")
    # time.sleep(1)

    # Example: Is Ganache Connected? - **************************
    result_ganache = is_ganache_connected()
    if result_ganache[0]:       # i.e. success = True
        st.info("Latest Block: " + str(result_ganache[1]))
        # Example: Ganache Transaction
        transaction_result = transaction_ganache(sender_account_ganache_09, sender_private_key_09, receiver_account_ganache_10)
        if transaction_result[0]:       # i.e. success = True
            st.info("Transaction Hash: " + str((transaction_result[2])))
            st.info("Current Balance of Sender: " + str(transaction_result[3]))
            st.info("Current Balance of Receiver: " + str(transaction_result[4]))
            st.balloons()
        else:
            st.error("Ganache Transaction Failed")
    else:
        st.error("Ganache is not connected")
    time.sleep(1)

elif choice == "Login":
    st.subheader("Please LogIn")
    comment_01 = '<p style="font-family:Sans; color:Red; font-size: 20px;">From here on out it is assumed that you have installed your Metamask wallet by now.</p>'
    comment_02 = '<p style="font-family:Sans; color:Red; font-size: 20px;">If not, then <b>STOP</b>. Install your Metamask wallet <b>BEFORE</b> proceeding.</p>'
    st.write(comment_01, unsafe_allow_html=True)
    st.write(comment_02, unsafe_allow_html=True)
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')

    if st.sidebar.button("Login"):
        st.success("Logged In as {}".format(username))
        st.warning("It is expected that you have installed your Metamask wallet.")


elif choice == "Signup":
    st.subheader("Create New Account")
    st.subheader("===== Some Samples To Look at =====")
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.0001)
        my_bar.progress(percent_complete + 1)
    st.spinner(text="In Progress ...")
    st.balloons()
    st.error("This is an error")
    st.warning("This is a warning")
    st.info("This is info")
    st.success("This is success")
    # https://docs.streamlit.io/library/api-reference/status/st.exception
    # st.exception("exception")
        
if __name__ == '__main__':
    main()
