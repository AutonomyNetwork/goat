import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from web3 import Web3
from web3.middleware.signing import construct_sign_and_send_raw_middleware
from eth_account.signers.local import LocalAccount
from eth_account import Account

from goat_adapters.langchain import get_on_chain_tools
from goat_plugins.erc20.token import  USDC, USDT, WBTC, ETH
from goat_plugins.erc20 import erc20, ERC20PluginOptions
from goat_wallets.evm import send_eth
from goat_wallets.web3 import Web3EVMWalletClient
from goat_plugins.coingecko import coingecko, CoinGeckoPluginOptions

# Initialize Web3 and account
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_PROVIDER_URL")))
private_key = os.getenv("WALLET_PRIVATE_KEY")
assert private_key is not None, "You must set WALLET_PRIVATE_KEY environment variable"
assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

account: LocalAccount = Account.from_key(private_key)
w3.eth.default_account = account.address  # Set the default account
w3.middleware_onion.add(
    construct_sign_and_send_raw_middleware(account)
)  # Add middleware

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini")


def main():
    # Get the prompt template
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("placeholder", "{chat_history}"),  # Prepend "Chat history:" to chat_history
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

    # Initialize tools with web3 wallet
    # wallet_client = Web3EVMWalletClient(w3)
    # if  hasattr(wallet_client, '_private_key'):
    #     print("Key exists in client")
    # else:
    #     print("Key does not exist in client")
    tools = get_on_chain_tools(
        wallet=Web3EVMWalletClient(w3),
        plugins=[
            send_eth(),
            erc20(options=ERC20PluginOptions(tokens=[USDC, USDT, WBTC , ETH])),
            coingecko(options=CoinGeckoPluginOptions(api_key=os.getenv("COINGECKO_API_KEY")))
        ],
    )
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)
    # chat_history = []  # Initialize an empty list to track chat history

    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        try:
            # chat_history.append({"role": "human", "content": user_input})

            response = agent_executor.invoke({
                "input": user_input,
                # "chat_history": chat_history,  # Static text and formatted chat history

            })

            print("\nAssistant:", response["output"])
        except Exception as e:
            print("\nError:", str(e))

def format_chat_history(chat_history):
    """
    Format the chat history into the correct string format for the prompt.
    Each entry in chat_history is a dictionary with 'role' and 'content' keys.
    """
    formatted_history = []
    for message in chat_history:
        formatted_history.append(f"{message['role'].capitalize()}: {message['content']}")
    return "\n".join(formatted_history)
if __name__ == "__main__":
    main()
