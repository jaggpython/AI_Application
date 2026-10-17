
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from backend.schemas import ChatRequest, ChatResponse

app = FastAPI(
    title="AI Chat Assistant API",
    description="Local AI chatbot using LangChain and Ollama",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.7,
)


@app.get("/")
def home():
    return {
        "message": "AI Chat Assistant API is running",
        "model": OLLAMA_MODEL,
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": OLLAMA_MODEL,
        "ollama_url": OLLAMA_BASE_URL,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        question = request.message.strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty.",
            )

        messages = [
            SystemMessage(
                content=(
                    "You are a helpful AI assistant. "
                    "Answer clearly and accurately. "
                    "Use Markdown when useful. "
                    "If you are uncertain, say so instead "
                    "of inventing facts."
                )
            )
        ]

        # Add recent conversation context.
        for item in request.history[-20:]:
            content = item.content.strip()

            if not content:
                continue

            if item.role == "user":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(AIMessage(content=content))

        messages.append(HumanMessage(content=question))

        result = llm.invoke(messages)

        return ChatResponse(
            answer=str(result.content)
        )

    except HTTPException:
        raise

    except Exception as exc:
        print(f"Chat error: {exc}")

        raise HTTPException(
            status_code=503,
            detail=(
                "Unable to generate a response. "
                "Check that Ollama is running and the "
                "configured model is installed."
            ),
        ) from exc
