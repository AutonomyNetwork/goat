from dotenv import load_dotenv
load_dotenv()
import os 
from fastapi import FastAPI,Request
from pydantic import BaseModel
from services.agent.chat import ChatAgent
from fastapi import APIRouter, Depends, HTTPException

class UserRequest(BaseModel):
    userId: str
    userSmartWalletAddress:str
    userMessage: str
    

app=FastAPI()

ORIGINAL_API_KEY = os.getenv("VALID_API_KEY")


def get_chat_agent() -> ChatAgent:
    return ChatAgent()


@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI app!"}

@app.get("/health")
def health():
    return {"message": "I am alive!"}

@app.post("/chat")
async def chat(
    request: Request,
    userRequest: UserRequest,
    chat_agent: ChatAgent = Depends(get_chat_agent)
):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is missing")
    if api_key != ORIGINAL_API_KEY:
        print(api_key,ORIGINAL_API_KEY,len(api_key),len(ORIGINAL_API_KEY))
        raise HTTPException(status_code=403, detail="Invalid API Key")

    if not userRequest.userId or not userRequest.userMessage or not userRequest.userSmartWalletAddress:
        raise HTTPException(status_code=400, detail="Invalid input")
    response = await chat_agent.chat_handler(userRequest.userMessage, userRequest.userId,userRequest.userSmartWalletAddress)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
