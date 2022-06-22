# import threading
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional
# from  etherscan import Etherscan
import requests
import json
from termcolor import colored, cprint
# import time
# import os

ETHAPI = 'key'
BSCAPI = 'key'

while True:    
    MNEMONIC: str = generate_mnemonic(language="english", strength=128)
    PASSPHRASE: Optional[str] = None  # "meherett"
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
    )
    bip44_hdwallet.clean_derivation()
    bip44_derivation: BIP44Derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=0, change=False, address=0)
    bip44_hdwallet.from_path(path=bip44_derivation)

    me = bip44_hdwallet.mnemonic()
    addr = bip44_hdwallet.address()

    # #ETH
    eth =requests.get(f'https://api.etherscan.io/api?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={ETHAPI}')
    ethJson =eth.json()
    dumpETHJson = json.dumps(ethJson)

    loadETHJson = json.loads(dumpETHJson)
    ethTransaction = loadETHJson["status"]
    if int(ethTransaction) >0:
        print(colored(f"Has transaction history {me} {addr}", color="green"))
        with open("valid.txt", "a") as ethWallets:
                ethWallets.write("\nWallet: " + me + " ETH CHAIN " + addr)
    else:
        print(colored(f"{ethTransaction} {me} {addr}", color="red"))

    #BSC
    bsc =requests.get(f'https://api.bscscan.com/api?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={BSCAPI}')
    bscJson =bsc.json()
    dumpBSCJson = json.dumps(bscJson)

    loadBSCJson = json.loads(dumpBSCJson)
    bscTransaction = loadBSCJson["status"]
    if int(bscTransaction) >0:
        print(colored(f"Has transaction history {me} {addr}", color="green"))
        with open("valid.txt", "a") as bscWallets:
                bscWallets.write("\nWallet: " + me + " BSC CHAIN " + addr)
    else:
        print(colored(f"{bscTransaction} {me} {addr}", color="red"))




    bip44_hdwallet.clean_derivation()
