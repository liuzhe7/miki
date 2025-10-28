from asyncio.log import logger
import uvicorn
from http_server import app

def main():
    """Start the HTTP server."""
    logger.info("Starting Miki User Input API server...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
