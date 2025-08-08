import json

from solcx import compile_standard, install_solc
from web3 import Web3
with open("./SimpleStorage.sol","r") as file:
    file_storage=file.read()

import  os
from dotenv import load_dotenv
load_dotenv()
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

w3=Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/96dda44d6be44c0dab2a3e5c9a8e6683"))
chain_id= 11155111
address="0x3d1E73b29515e01CE0D4793a3290F8f9AA664b44"
private_key=os.getenv("PRIVATE_KEY")

SimpleStorage=w3.eth.contract(abi=abi,bytecode=bytecode)
nonce= w3.eth.get_transaction_count(address)
transaction=SimpleStorage.constructor().build_transaction({
    "chainId":chain_id,"from":address,"nonce":nonce
})

singed_tc=w3.eth.account.sign_transaction(transaction,private_key=private_key)
hash_transaction=w3.eth.send_raw_transaction(singed_tc.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(hash_transaction)

simple_contract=w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)

transaction2 = simple_contract.functions.store(15).build_transaction({
  "chainId":chain_id,"from":address,"nonce":nonce+1
})
singed_tc2=w3.eth.account.sign_transaction(transaction2,private_key=private_key)
hased_tr=w3.eth.send_raw_transaction(singed_tc2.raw_transaction)
tx_receipt2 = w3.eth.wait_for_transaction_receipt(hased_tr)
print(tx_receipt2)
print(simple_contract.functions.retrieve().call())