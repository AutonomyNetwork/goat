from typing import Dict, List, TypedDict


class ChainData(TypedDict):
    contractAddress: str


class Token(TypedDict):
    decimals: int
    symbol: str
    name: str
    chains: Dict[int, ChainData]


class ChainSpecificToken(TypedDict):
    chain_id: int
    decimals: int
    symbol: str
    name: str
    contract_address: str


PEPE: Token = {
    "decimals": 18,
    "symbol": "PEPE",
    "name": "Pepe",
    "chains": {
        1: {"contractAddress": "0x6982508145454Ce325dDbE47a25d4ec3d2311933"},
        10: {"contractAddress": "0xc1c167cc44f7923cd0062c4370df962f9ddb16f5"},
        8453: {"contractAddress": "0xb4fde59a779991bfb6a52253b51947828b982be3"},
    },
}

DEDE: Token = {
    "decimals": 18,
    "symbol": "DEDE",
    "name": "DEDE",
    "chains": {
        11155111: {"contractAddress": "0xa4cd5DCF7A1106BC2be45e3280B376D2096346CF"},
    },
}

DUMMY: Token = {
    "decimals": 18,
    "symbol": "DUMMY",
    "name": "Dummy",
    "chains": {
        200901: {"contractAddress": "0x11c683DEB1d28C6b48725e7d02fB9FE89D1CfE04"},
    },
}

USDC: Token = {
    "decimals": 6,
    "symbol": "USDC",
    "name": "USDC",
    "chains": {
        1: {"contractAddress": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"},
        10: {"contractAddress": "0x0b2c639c533813f4aa9d7837caf62653d097ff85"},
        137: {"contractAddress": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359"},
        8453: {"contractAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"},
        84532: {"contractAddress": "0x036CbD53842c5426634e7929541eC2318f3dCF7e"},
        11155111: {"contractAddress": "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"},
        34443: {"contractAddress": "0xd988097fb8612cc24eeC14542bC03424c656005f"},
        200901: {"contractAddress": "0xf8c374ce88a3be3d374e8888349c7768b607c755"},
    },
}

ETH: Token = {
    "decimals": 18,
    "symbol": "ETH",
    "name": "Ethereum",
    "chains": {
        200901: {"contractAddress": "0xef63d4e178b3180beec9b0e143e0f37f4c93f4c2"},
    },
}

USDT: Token = {
    "decimals": 6,
    "symbol": "USDT",
    "name": "USDT",
    "chains": {
        200901: {"contractAddress": "0xfe9f969faf8ad72a83b761138bf25de87eff9dd2"},
    },
}

WBTC: Token = {
    "decimals": 18,
    "symbol": "WBTC",
    "name": "Wrapped Bitcoin",
    "chains": {
        200901: {"contractAddress": "0xff204e2681a6fa0e2c3fade68a1b28fb90e4fc5f"},
    },
}

MODE: Token = {
    "decimals": 18,
    "symbol": "MODE",
    "name": "Mode",
    "chains": {
        34443: {"contractAddress": "0xDfc7C877a950e49D2610114102175A06C2e3167a"},
    },
}


def get_tokens_for_network(
    chain_id: int, tokens: List[Token]
) -> List[ChainSpecificToken]:
    result: List[ChainSpecificToken] = []

    for token in tokens:
        chain_data = token["chains"].get(chain_id)
        if chain_data:
            result.append(
                {
                    "chain_id": chain_id,
                    "decimals": token["decimals"],
                    "symbol": token["symbol"],
                    "name": token["name"],
                    "contract_address": chain_data["contractAddress"],
                }
            )

    return result
