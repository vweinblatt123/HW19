# Import dependencies
import os
import subprocess
import json
from dotenv import load_dotenv

# Load and set environment variables
load_dotenv("mnemonic.env")
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import *
from web3 import Web3
from bit import wif_to_key, PrivateKeyTestnet, network
 
# Create a function called `derive_wallets`
def derive_wallets(coin):
    command = 'php hd-wallet-derive.php -g --mnemonic="' + mnemonic + '" --cols=address,index,path,privkey,pubkey,pubkeyhash,xprv,xpub --format=json --numderive=3 --coin=' + coin
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {"btc-test" : derive_wallets(BTCTEST),
         "eth"      : derive_wallets(ETH) }
#print(coins)

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    return PrivateKeyTestnet(priv_key)
   

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    return account.prepare_transaction(account.address, [(to, amount, BTC)])
    # YOUR CODE HERE
    

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    raw_tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(raw_tx)
    return network.NetworkAPI.broadcast_tx_testnet(signed_tx)

    
# account_obj = priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey'])
# sent = send_tx(BTCTEST, account_obj, coins[BTCTEST][1]['address'], 0.00001)
