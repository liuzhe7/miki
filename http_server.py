"""
HTTP Server for receiving user input.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import logging
from pathlib import Path
from langchain_core.runnables.config import RunnableConfig

import tools
from agent import agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Create FastAPI app
app = FastAPI(
    title="Miki User Input API",
    description="API for receiving and processing user input",
    version="1.0.0"
)

# Mount static files directory
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class UserInput(BaseModel):
    """User input request model."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "input": "What's the weather like today?"
            }
        }
    )

    input: str = Field(..., description="User input text", min_length=1)


class UserInputResponse(BaseModel):
    """Response model for user input."""
    success: bool
    message: str
    request_id: str
    timestamp: str
    received_input: UserInput
    ai_response: Optional[str] = Field(default=None, description="AI model response")


@app.get("/")
async def root():
    """Root endpoint - HTML page for user input."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/input", response_model=UserInputResponse)
async def receive_user_input(user_input: UserInput):
    """
    Receive and process user input.
    
    Args:
        user_input: UserInput model containing user_id, input text, and optional metadata
        
    Returns:
        UserInputResponse with success status and details
    """
    try:
        # Generate a unique request ID
        request_id = f"req_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        # Log the received input
        logger.info(f"Received input: {user_input.input[:50]}...")
        
        # Call the AI agent with user input
        logger.info("Invoking AI agent...")
        config: RunnableConfig = {"configurable": {"thread_id": request_id}}
        
        agent_response = agent.invoke(
            {"messages": [{"role": "user", "content": user_input.input}]},
            config=config,
            context=tools.Context(user_id=request_id),
        )
        
        # Extract the AI response
        ai_response_text = None
        if "structured_response" in agent_response:
            response_obj = agent_response["structured_response"]
            ai_response_text = response_obj.msg
        elif "messages" in agent_response and agent_response["messages"]:
            # Get the last message from the agent
            last_message = agent_response["messages"][-1]
            if hasattr(last_message, "content"):
                ai_response_text = last_message.content
            elif isinstance(last_message, dict) and "content" in last_message:
                ai_response_text = last_message["content"]
        
        logger.info(f"AI response received: {ai_response_text[:100] if ai_response_text else 'None'}...")
        
        response = UserInputResponse(
            success=True,
            message="User input received and processed successfully",
            request_id=request_id,
            timestamp=datetime.now().isoformat(),
            received_input=user_input,
            ai_response=ai_response_text
        )
        
        logger.info(f"Successfully processed request {request_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing user input: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process user input: {str(e)}"
        )
