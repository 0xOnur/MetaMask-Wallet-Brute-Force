import requests
import json
from termcolor import colored, cprint
import winsound
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from typing import Optional

PASSPHRASE: Optional[str] = None

bscAPI = "key"
ethAPI = "key"
avaxAPI = "key"
polyAPI = "key"

duration = 2000
freq = 900

count = 0
with open("walletsBeCheck.txt", "r+") as file:
    while True:
        wallet = file.readline()
        words = wallet.split(' ')
        myMnemonic = words[0] + ' ' + words[1] + ' ' + words[2] + ' ' + words[3] + ' ' + words[4] + ' ' + words[5] + ' ' + words[6] + ' ' + words[7] + ' ' + words[8] + ' ' + words[9] + ' ' + words[10] + ' ' + words[11]

        # Initialize Ethereum mainnet BIP44HDWallet
        bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
        # Get Ethereum BIP44HDWallet from mnemonic
        bip44_hdwallet.from_mnemonic(mnemonic=myMnemonic[:-1], language="english", passphrase=PASSPHRASE)
        # Clean default BIP44 derivation indexes/paths
        bip44_hdwallet.clean_derivation()
        
        # Get Ethereum BIP44HDWallet information's from address index
        bip44_derivation: BIP44Derivation = BIP44Derivation(
                cryptocurrency=EthereumMainnet, account=0, change=False, address=0)
        bip44_hdwallet.from_path(path=bip44_derivation)
        
        
        #API CHECK WALLETS
            
        #BSC
        bsc = requests.get(f'https://api.bscscan.com/api?module=account&action=balance&address={bip44_hdwallet.address()}&apikey={bscAPI}')
        bscJson = bsc.json()
        dumpBSCJson = json.dumps(bscJson)

        loadBSCJson = json.loads(dumpBSCJson)
        bscBalance = loadBSCJson["result"]
        print("BSC:"+bscBalance)
        if int(bscBalance) > 0:
            print(colored("money", color="green"))
            winsound.Beep(freq, duration)
            with open("checkedWallets.txt", "a") as bscWallets:
                bscWallets.write("\nWallet: " + wallet + " BSC CHAIN " + bip44_hdwallet.address())
        else:
            print(colored("nothing", color="red"))


        #ETH
        eth =requests.get(f'https://api.etherscan.io/api?module=account&action=balance&address={bip44_hdwallet.address()}&apikey={ethAPI}')
        ethJson =eth.json()
        dumpETHJson = json.dumps(ethJson)

        loadETHJson = json.loads(dumpETHJson)
        ethBalance = loadETHJson["result"]
        print("ETH:"+ethBalance)
        if int(ethBalance) > 0:
            print(colored("money", color="green"))
            winsound.Beep(freq, duration)
            with open("checkedWallets.txt", "a") as ethWallets:
                ethWallets.write("\nWallet: " + wallet + "ETH CHAIN " + bip44_hdwallet.address())
        else:
            print(colored("nothing", color="red"))

        #AVAX
        avax = requests.get(f'https://api.snowtrace.io/api?module=account&action=balance&address={bip44_hdwallet.address()}&apikey={avaxAPI}')
        avaxJson = avax.json()
        dumpAvaxJson = json.dumps(avaxJson)

        loadAvaxJson = json.loads(dumpAvaxJson)
        avaxBalance = loadAvaxJson['result']
        print("AVAX:"+avaxBalance)
        if int(avaxBalance) > 0:
            print(colored("money", color="green"))
            winsound.Beep(freq, duration)
            with open("checkedWallets.txt", "a") as avaxWallets:
                avaxWallets.write("\nWallet: " + wallet + "AVAX CHAIN " + bip44_hdwallet.address())
        else:
            print(colored("nothing", color="red"))
            
        #POLYGON
        polygon = requests.get(f'https://api.polygonscan.com/api?module=account&action=balance&address={bip44_hdwallet.address()}&apikey={polyAPI}')
        polyJson = polygon.json()
        dumpPolyJson = json.dumps(polyJson)

        loadPolyJson = json.loads(dumpPolyJson)
        polyBalance = loadPolyJson['result']
        print("MATİC:"+polyBalance)
        if int(polyBalance) > 0:
            print(colored("money", color="green"))
            winsound.Beep(freq, duration)
            with open("checkedWallets.txt", "a") as polyWallets:
                polyWallets.write("\nWallet: " + wallet + "POLYGON CHAIN " + bip44_hdwallet.address())
        else:
            print(colored("nothing", color="red"))


        count+=1
        print(f'CHECKED:{count}')
        print(f"{bip44_hdwallet.mnemonic()} {bip44_hdwallet.address()}")
        print("")
        bip44_hdwallet.clean_derivation()
