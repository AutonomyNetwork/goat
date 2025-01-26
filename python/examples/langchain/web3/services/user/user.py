import os
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware.signing import construct_sign_and_send_raw_middleware
from eth_account.signers.local import LocalAccount
from eth_account import Account
# Load environment variables
load_dotenv()

import requests

async def get_user_private_key(userId:str):
    try:
        data={
        "userId": userId
        }
        web3_auth_api_key=os.getenv("WEB3_AUTH_API_KEY")
        headers={
        'Content-Type':'application/json',
        'x-api-key': web3_auth_api_key
        }
        web3_auth_domain=os.getenv("WEB3_AUTH_DOMAIN")
        print("FFFFFFFFFFFFFFFFFFFFFFFFFFF",web3_auth_domain)
        response=requests.api.post(f"""{web3_auth_domain}/create_wallet""",headers=headers,json=data)
        print(response,"RESPONSEEEEEEEEEEEEEEEEEEEEEEEE")
        if response.status_code==200:
            print(response.json().get('privateKey'))
            return response.json().get('privateKey')
        
    except Exception as e:
        print(e)
        raise e

async def get_user_wallet_client(w3: Web3, user_id: str) -> Web3:
    """
    Sets up a Web3 client with a user's wallet configured.

    Args:
        w3 (Web3): A Web3 instance.
        private_key (str): The private key of the user.

    Returns:
        Web3: The Web3 instance with the user's wallet configured.
    """
    try:
        private_key=await get_user_private_key(user_id)
        print(private_key,"FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        # Create a local account from the private key
        account: LocalAccount = Account.from_key(private_key)
        
        # Set the default account for the Web3 instance
        w3.eth.default_account = account.address
        
        # Add the middleware to handle signing and sending raw transactions
        w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
        print(w3)
        return w3
    except Exception as e:
        raise RuntimeError(f"Failed to set up the wallet client: {e}")