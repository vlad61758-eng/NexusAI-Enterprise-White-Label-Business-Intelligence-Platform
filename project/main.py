import asyncio
import logging
from dotenv import load_dotenv

from db import init_db
from hunter import run_hunter
from executor import run_executor

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Initializing system...")

    # Load environment variables
    load_dotenv()

    # Initialize the database
    await init_db()

    logger.info("Starting Hunter and Executor concurrently...")

    # Run both the telethon client (hunter) and the aiogram loop (executor) concurrently
    # asyncio.gather allows them to run in the same event loop
    await asyncio.gather(
        run_hunter(),
        run_executor()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("System shutting down due to keyboard interrupt.")
    except Exception as e:
        logger.error(f"Critical error: {e}")
