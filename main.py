from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize ChatOpenAI
chat_model = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Store conversation history in memory
conversation_history: List[Dict] = []

class ChatMessage(BaseModel):
    user_message: str

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(message: ChatMessage):
    try:
        # Convert conversation history to LangChain message format
        messages = []
        for msg in conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        # Add current message
        messages.append(HumanMessage(content=message.user_message))
        
        # Get response from ChatOpenAI
        response = chat_model.invoke(messages)
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": message.user_message})
        conversation_history.append({"role": "assistant", "content": response.content})
        
        return {"assistant_message": response.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API del Chatbot",
        "endpoints": {
            "chat": "/chat - POST para enviar mensajes",
            "health": "/health - GET para verificar el estado"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 