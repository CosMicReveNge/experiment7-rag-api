import logging
import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr

from support_rag import generate_answer

# Load environment variables from .env.
load_dotenv()

# Configure basic logging for API requests.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Customer Support RAG API",
    description="A simple API with validation, logging, and error handling.",
    version="1.0.0"
)


class AskRequest(BaseModel):
    # Reject empty questions and limit input to 1000 characters.
    question: constr(strip_whitespace=True, min_length=1, max_length=1000)


@app.get("/")
def home():
    # Display basic information about the API.
    return {
        "message": "Customer Support RAG API is running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    # Check whether the API process is responding.
    return {"status": "healthy"}


@app.post("/ask")
def ask_question(request: AskRequest):
    # Start measuring the response time.
    start_time = time.perf_counter()

    try:
        # Generate an answer using the RAG module.
        answer = generate_answer(request.question)

        # Calculate elapsed time in milliseconds.
        elapsed_ms = round(
            (time.perf_counter() - start_time) * 1000, 2
        )

        # Log successful requests without storing question contents.
        logging.info(
            "Request successful | latency_ms=%.2f",
            elapsed_ms
        )

        return {
            "question": request.question,
            "answer": answer,
            "response_time_ms": elapsed_ms
        }

    except Exception:
        # Log the failure while hiding internal details from clients.
        elapsed_ms = round(
            (time.perf_counter() - start_time) * 1000, 2
        )

        logging.exception(
            "Request failed | latency_ms=%.2f",
            elapsed_ms
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error. Please try again later."
        )
