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
from services.agent.prompt import SystemPrompt

from services.memory.mem0 import MemoryManager
from config import AGENT_ID
from services.user.user import get_user_wallet_client,get_user_private_key

class ChatAgent:
    def __init__(self):
        self.llm= ChatOpenAI(model="gpt-4o-mini")
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_PROVIDER_URL")))
        self.mem0=MemoryManager(mem0_api_key=os.getenv("MEM0_API_KEY"))



    async def chat_handler(self, user_message:str,user_id:str,user_smart_wallet:str):
        try:
            sytem_prompt= SystemPrompt.get_blay_system_prompt()
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", sytem_prompt),
                    ("system", "Chat History:\n{chat_history}"),  # Dynamic chat history placeholder
                    ("human", "{input}"),  # User's input
                    ("placeholder", "{agent_scratchpad}"),  # Agent's scratchpad
                ]
            )
            print(prompt,"PROMPT")

            tools = await self.get_agent_tools(self.w3,user_id)
            agent = create_tool_calling_agent(self.llm, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)
            recent_memories =  await self.mem0.search_recent_user_memory(user_id=user_id,agent_id=AGENT_ID)
            print(recent_memories,"RECENT MEMORIES")
            response = agent_executor.invoke({
                "input": user_message, 
                "chat_history": recent_memories,  # Static text and formatted chat history

            })
            message=[
                {
                "role":"user",
                "content":user_message,
                },
                {
                "role":"assistant",
                "content":response["output"]
                }
            ]

            await self.mem0.add_user_memory(user_id=user_id, message=message,infer=False,agent_id=AGENT_ID)
            print(response['output'],"RESPONSE")
            return response["output"]
        except Exception as e:
            print(e)
            raise

    async def get_agent_tools(self,w3,user_id):
        print(w3,"W##############")
        final_w3 = await get_user_wallet_client(w3,user_id) 
        tools = get_on_chain_tools(
        wallet=Web3EVMWalletClient(final_w3),
        plugins=[
            send_eth(),
            erc20(options=ERC20PluginOptions(tokens=[USDC, USDT, WBTC , ETH])),
            coingecko(options=CoinGeckoPluginOptions(api_key=os.getenv("COINGECKO_API_KEY")))
        ],
        )
        return tools

# if __name__ == "__main__":
#     chat=Chat()
#     chat.chat_handler("hello","123")