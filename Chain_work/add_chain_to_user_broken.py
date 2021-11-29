from dataclasses import replace
import streamlit as st
import pandas as pd
import hashlib
import sqlite3
import streamlit.components.v1 as stc
import dataclasses_sql
import dill as pickle
from numpy.core.records import record
				
from datetime import datetime
from dataclasses import dataclass
from typing import Any, List

import hashlib
import requests
import os

#global st

# Security
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# Database Management
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY,password TEXT)')
	


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	
	data = c.fetchall()
	
	return data
	

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



@dataclass
class RecordTransaction:
	amount: float
	ded_type: str
	description: str
	receipt: str
	occupation: str
	quarter: str

# Our Block class
@dataclass
class Block:
	record: RecordTransaction
	trade_time: str = datetime.utcnow().strftime("%H:%M:%S")
	prev_hash: str = 0

	def hash_block(self):
		# Declare a hashing algorithm
		sha = hashlib.sha256()

		# Encode the time of trade
		trade_time_encoded = self.trade_time.encode()
		# Add the encoded trade time into the hash
		sha.update(trade_time_encoded)

		# Encode the Record class
		record = str(self.record).encode()
		# Then hash it
		sha.update(record)

		prev_hash = str(self.prev_hash).encode()
		sha.update(prev_hash)

		# Return the hash to the rest of the Block class
		return sha.hexdigest()
# Building Blocks Dataclass?
@dataclass
class BuildingBlock:
	record: RecordTransaction
	trade_time: str
	prev_hash: str

	def hash_block(self):
		# Declare a hashing algorithm
		sha = hashlib.sha256()

		# Encode the time of trade
		trade_time_encoded = self.trade_time.encode()
		# Add the encoded trade time into the hash
		sha.update(trade_time_encoded)

		# Encode the Record class
		record = str(self.record).encode()
		# Then hash it
		sha.update(record)

		prev_hash = str(self.prev_hash).encode()
		sha.update(prev_hash)

		# Return the hash to the rest of the Block class
		return sha.hexdigest()

# Our StockChain class
from typing import List
@dataclass
class StockChain:
	# The class `StockChain` holds a list of blocks
	chain: List[Block]
	# The function `add_block` adds any new `block` to the `chain` list
	def add_block(self, block):
		self.chain += [block]

@dataclass
class BuildingChain:
	# The class `StockChain` holds a list of blocks
	chain: List[BuildingBlock]
	# The function `add_block` adds any new `block` to the `chain` list
	def add_block(self, block):
		self.chain += [block]

def recreate_record(df):
	for i in range(len(df)):
		re_records = [RecordTransaction(
			amount=df.iloc[i,0],
			ded_type = df.iloc[i,1],
			description=df.iloc[i,3],
			receipt= df.iloc[i,3],
			occupation= df.iloc[i,4],
			quarter= df.iloc[i,5]

		)]
	return re_records

def recreate_block(df):
	for i in df:
		blocks = BuildingBlock(
		record = recreate_record(df),
		trade_time = df.loc[i,6],
		prev_hash = df.loc[i,7]
		)
	return blocks

def recreate_chain(df):
	chain = BuildingChain()

def main():

	"""Simple Login App"""

	st.title("Write-Off Warrior")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			
			create_usertable()

			# Create SQL table to hold chain df
			c.execute('''CREATE TABLE IF NOT EXISTS chaintable(
			amount FLOAT,
			ded_type TEXT,
			description TEXT,
			receipt TEXT,
			occupation TEXT,
			quarter TEXT,
			trade_time TEXT,
			prev_hash TEXT,
			username TEXT,
			FOREIGN KEY (username) REFERENCES userstable(username))''')

			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			
			if result:
				# Import required libraries
				
				from dotenv import load_dotenv

				# Import infura API info(SW: At some point need to figure out how to get Infura API info to talk to app w/o showing it on github)
				load_dotenv()
				infura_id = os.getenv("INFURA_WOW_ID")
				infura_private = os.getenv("INFURA_WOW_PRIVATE")

				
				
				
				

			

				# Add text titles to the web page
				st.markdown("# Welcome to Write-Off Warrior")
				st.subheader("Upload Receipt Picture")
				image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

				if image_file is not None:

					# To See details
					file_details = {"filename":image_file.name, "filetype":image_file.type,
											"filesize":image_file.size}
					st.write(file_details)

					# To View Uploaded Image
				if image_file is not None:
					st.image(image_file, width=250)

					# Save image to temp Dir
					with open(os.path.join("Receipts",image_file.name), "wb") as f:
						f.write(image_file.getbuffer())

						st.success("File Saved")
					path = (f"Receipts/{image_file.name}")
					ipfs_file ={
						'file' : path
					}
					# Send file to Infura
					response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files=ipfs_file, auth=(infura_id,infura_private))
					st.write(response.text)
				st.markdown("In order for us to assist you, please fill out the information below. ")

				##
				page_names= ['Self-Employed', 'Small Business Owner','Employed by an Institution']
				page= st.radio ('What is your employment status?', page_names)
				st.write("**Your employment status is:**", page)


				if page == 'Self-Employed':
					occupation = st.text_input('What is your business?')
					ded_type = st.selectbox(
					'Type of Deduction',
					('Vehicle Expense', 'Employee Pay', 'Travel, Meals, Entertainment Expenses', 'Home Office Deduction', 'Office Supplies','Memberships Dues/Fees')
				)
					description = st.text_input("Description of Purchase")
					amount = st.text_input("Amount")
					receipt = st.text_input("Receipt Hash")
					quarter = st.text_input("What quarter does this deduction affect?")

				elif page == 'Small Business Owner':
					occupation = st.text_input("What is your business?")
					ded_type = st.selectbox(
					'Type of Deduction',
					('Vehicle Expense', 'Educator Expense (max $250)', 'Employee Pay', 'Travel, Meals, Entertainment Expenses', 'Home Office Deduction', 'Office Supplies','Memberships Dues/Fees')
				)
					description = st.text_input("Description of Purchase")
					amount = st.text_input("Amount")
					receipt = st.text_input("Receipt Hash")
					
				else:
					occupation = st.selectbox('What is your occupation?',
					('Teacher', 'Other'))
					ded_type = st.selectbox('Type of Deduction',
					('Vehicle Expense', 'Educator Expense (max $250)', 'Employee Pay', 'Travel, Meals, Entertainment Expenses', 'Home Office Deduction', 'Office Supplies','Memberships Dues/Fees'))
					description = st.text_input("Description of Purchase")
					amount = st.text_input("Amount")
					receipt = st.text_input("Receipt Hash")
				

				# Set up the web app for deployment (including running the StockChain class)
				@st.cache(allow_output_mutation=True)
				def setup():
					# Try to see if user already has a table
					# c.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name="userstable"''')
					# c.execute('''SELECT * FROM chaintable INNER JOIN userstable ON chaintable.username = userstable.username;''')
					# resso = c.fetchall()
					# for row in resso:
					# 	st.write(row)

					# Try to unpickle a file and rebuild the StockChain
					try:
						unpickled_df = pd.read_pickle(f"pickles/{username}")
						re_record = RecordTransaction(
							amount=unpickled_df.iloc[-1,0],
							ded_type = unpickled_df.iloc[-1,1],
							description = unpickled_df.iloc[-1, 2],
							receipt = unpickled_df.iloc[-1,3],
							occupation = unpickled_df.iloc[-1,4],
							quarter = unpickled_df.iloc[-1, 5]
						)
						regenesis_block = BuildingBlock(
							record = re_record,
							trade_time = unpickled_df.iloc[-1, 6],
							prev_hash = unpickled_df.iloc[-1, 7]	
						)
						return BuildingChain([regenesis_block])
					except:	
						genesis_block = Block(
							record=RecordTransaction(amount=0, ded_type="N/a", description="N/A", receipt="N/A", occupation="N/A", quarter = "N/A")
						)
						return StockChain([genesis_block])

				# Serve the web app
                
				stockchain_live = setup()

				# Add a button using Streamlit to add a new block to the chain
				if st.button("Add Block"):
					# Pull the original block to start on
					prev_block = stockchain_live.chain[-1]
					st.write(type(prev_block))

					# Hash the original block (to put into the next block)
					# if prev_block == (type(BuildingBlock)):
					# 	prev_block_hash = prev_block.hash_block()
					# else:
					prev_block_hash = prev_block.hash_block()

					# Create a `new_block` so that shares, buyer_id, and seller_id from the user input are recorded as a new block
					new_block = Block(
						# data=input_data,
						record=RecordTransaction(amount, ded_type, description, receipt, occupation, quarter),
						prev_hash=prev_block_hash
					)

					# Add the new_block to the existing chain
					stockchain_live.add_block(new_block)
                    # print(new_block)

					# Save the chain as a df and pickle
					stockchain_df = pd.DataFrame(stockchain_live.chain)
					stockchain_df.loc[:,"username"] = username
					chain_recs = stockchain_df["record"]
					chain_df = pd.DataFrame(list(chain_recs))
					chain_df_no_recs = stockchain_df.drop(columns="record")
					full_chain_df= pd.concat([chain_df, chain_df_no_recs],axis=1)
					# pickle_file = open(f"{username}.pkl", 'wb')
					# pickled_info = pickle.dumps(stockchain_live.chain)
					# pikk = pickle.loads(pickled_info)
					# st.write(pikk)
					full_chain_df.to_pickle(f"pickles/{username}")
					unpickled_df = pd.read_pickle(f"pickles/{username}")
					st.write(unpickled_df.iloc[-1, 0])

					# latest_chain = stockchain_live
					
					# c.execute('''INSERT INTO userstable(chain) VALUES (?)''', latest_chain)
					# st.text(type(latest_chain))
					# st.text(username)
					
					# pickle_file.close()

					# Just for fun, we add a little pizzazz
					st.balloons()

				if st.button("unpickle chain"):
					unpickled_df = pd.read_pickle(f"pickles/{username}")
					re_record = RecordTransaction(
							amount=unpickled_df.iloc[-1,0],
							ded_type = unpickled_df.iloc[-1,1],
							description = unpickled_df.iloc[-1, 2],
							receipt = unpickled_df.iloc[-1,3],
							occupation = unpickled_df.iloc[-1,4],
							quarter = unpickled_df.iloc[-1, 5]
						)
					
					regenesis_block = BuildingBlock(
					record = re_record,
					trade_time= unpickled_df.iloc[-1,6],
					prev_hash= unpickled_df.iloc[-1,7]	
					)
					return BuildingChain([regenesis_block])
					
				if st.button('rebuild chain'):
					unpickled_df = pd.read_pickle(f"pickles/{username}")
					# st.text(unpickled_df)
					chain = recreate_record(unpickled_df)
					st.write('records')
					st.write(chain)
				# Attempt a button to check shares
				if st.button("Check Total Deductions"):
					total_deductions = 0.0
					for block in stockchain_live.chain:
						total_deductions += float(block.record.amount)
					st.write(total_deductions)

				# Add a title for the chain display section
				st.markdown("## The Stockchain Ledger")

				# Save the data from the blockchain as a DataFrame
				stockchain_df = pd.DataFrame(stockchain_live.chain)
				stockchain_df.loc[:,"username"] = username
				# recs = stockchain_df
				st.write(stockchain_df)
				st.write(stockchain_df["record"])
				chain_recs = stockchain_df["record"]
				chain_df = pd.DataFrame(list(chain_recs))
				chain_df_no_recs = stockchain_df.drop(columns="record")
				full_chain_df= pd.concat([chain_df, chain_df_no_recs],axis=1)
				# pickle_file = open(f"username", 'wb')
				# pickled_info = pickle.dumps(full_chain_df)
				full_chain_df.to_pickle(f"pickles/{username}")
				unpickled_df = pd.read_pickle(f"pickles/{username}")
				st.write(unpickled_df.iloc[-1, 0])
				# for row in chain_recs:
					# amount = []
					# ded_type = []
					# description = []
					# receipt = []
					# occupation = []
					# quarter = []
				# 	record_data.append(
				# 		{
				# 			"amount" : amount,
				# 			'ded_type' : ded_type,
				# 			'description' : description,
				# 			'receipt' : receipt,
				# 			'occupation' : occupation,
				# 			'quarter' : quarter
				# 		}
				# 	)
				# recorddf = pd.DataFrame(record_data)
				st.write(full_chain_df)
			


				# Add stockchain_df to SQL table
				# full_chain_df.to_sql('chaintable', con = conn, if_exists='replace')
				# results = c.execute('''SELECT * FROM chaintable''').fetchall()

				# st.write(results)

				# Trying to rebuild blockchain from df
				# chain_recs = stockchain_df["record"]
				# chain_time = stockchain_df["trade_time"]
				# chain_hash = stockchain_df["prev_hash"]
				# for rec in chain_recs:
				# 	old_recs = RecordTransaction(amount=rec["amount"],
				# 	ded_type=rec['ded_type'],
				# 	description=rec["description"],
				# 	receipt=rec['receipt'],
				# 	occupation=rec['occupation'],
				# 	quarter=rec['quarter'])
				# 	# st.write(old_recs)
				# for block in stockchain_df:
				# 	building_blocks = BuildingBlock(
				# 		record = old_recs,
				# 		trade_time = stockchain_df["trade_time"],
				# 		prev_hash = stockchain_df["prev_hash"],
					# )
				# st.write(building_blocks.record)

				# stock_json = stockchain_df.to_json()

				# st.text(stock_json[2])

				# for element in stockchain_df:
				#     st.text(element)
				# Display the DataFrame data
				# st.write(stockchain_df)
				# st.write(Block.record.shares)

				# Add a dropdown menu to allow users to select which block in the chain to display
				st.sidebar.write("# Block Inspector")
				selected_block = st.sidebar.selectbox(
					"Which block would you like to see?", stockchain_live.chain
				)

				# Display the selected block on the sidebar
				st.sidebar.write(selected_block)		
				# Ad julia code here

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
				if task == "Add Post":
					st.subheader("Add Your Post")

				elif task == "Analytics":
					st.subheader("Analytics")
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()