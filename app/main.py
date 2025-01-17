from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, AsyncGenerator
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

@app.post("/chat/stream")
async def chat_stream(message: ChatMessage):
    try:
        # Usar el mismo chat_model pero con streaming
        streaming_model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            streaming=True
        )
        
        # Convertir historial y preparar mensajes
        messages = []
        for msg in conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        messages.append(HumanMessage(content=message.user_message))

        # Actualizar conversation_history con el mensaje del usuario
        conversation_history.append({"role": "user", "content": message.user_message})

        async def generate_response() -> AsyncGenerator[str, None]:
            full_response = ""
            async for chunk in streaming_model.astream(messages):
                if chunk.content:
                    full_response += chunk.content
                    yield f"data: {chunk.content}\n\n"
            # Actualizar conversation_history con la respuesta completa
            conversation_history.append({"role": "assistant", "content": full_response})

        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream"
        )
        
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