import json

from solcx import compile_standard, install_solc
from web3 import Web3
with open("./SimpleStorage.sol","r") as file:
    file_storage=file.read()

import  os
from dotenv import load_dotenv
load_dotenv()
## compile code
compiler= compile_standard(
    {
        "language":"Solidity",
        "sources":{"SimpleStorage.sol":{"content":file_storage}},
        "settings":{
            "outputSelection":{
                "*":{"*":["abi","metadata","evm.bytecode","evm.sourceMap"]}
            }
        }
    }
    ,
    solc_version="0.6.0"
)

with open("compiled_conde.json","w") as file:
    json.dump(compiler,file)

bytecode=compiler["contracts"]["SimpleStorage.sol"]["SimpleContract"]["evm"]["bytecode"]["object"]

abi=compiler["contracts"]["SimpleStorage.sol"]["SimpleContract"]["abi"]

## create w3
w3=Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/96dda44d6be44c0dab2a3e5c9a8e6683"))
chain_id= 11155111
address="0x3d1E73b29515e01CE0D4793a3290F8f9AA664b44"
private_key=os.getenv("PRIVATE_KEY")

## create the contract
SimpleStorage=w3.eth.contract(abi=abi,bytecode=bytecode)
nonce= w3.eth.get_transaction_count(address)
## create the transaction
transaction=SimpleStorage.constructor().build_transaction({
    "chainId":chain_id,"from":address,"nonce":nonce
})
##sign the transaction
singed_tc=w3.eth.account.sign_transaction(transaction,private_key=private_key)

# send the transaction
hash_transaction=w3.eth.send_raw_transaction(singed_tc.raw_transaction)

# wait until the transaction is injected into a blockchain
tx_receipt = w3.eth.wait_for_transaction_receipt(hash_transaction)

## now we  get the contract from the blockchain
simple_contract=w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)

## create new transaction for executing of a function
transaction2 = simple_contract.functions.store(15).build_transaction({
  "chainId":chain_id,"from":address,"nonce":nonce+1
})
singed_tc2=w3.eth.account.sign_transaction(transaction2,private_key=private_key)
hased_tr=w3.eth.send_raw_transaction(singed_tc2.raw_transaction)
tx_receipt2 = w3.eth.wait_for_transaction_receipt(hased_tr)

print(tx_receipt2)
## make call function this one doesn't make a transaction
print(simple_contract.functions.retrieve().call())