import asyncio
import logging
import signal
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config.settings import BOT_TOKEN, LOGGING_LEVEL, LOGGING_FORMAT
from database import init_db, migrate_db
from middleware import ThrottlingMiddleware, SubscriptionMiddleware, BanCallbackMiddleware
from handlers import register_handlers

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOGGING_LEVEL),
    format=LOGGING_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Global shutdown event
shutdown_event = asyncio.Event()


async def set_bot_commands():
    """Set bot commands for menu"""
    try:
        await bot.set_my_commands([
            BotCommand(command="start", description="Главное меню"),
            BotCommand(command="help", description="Помощь"),
        ])
        logger.info("Bot commands set successfully")
    except Exception as e:
        logger.error(f"Error setting bot commands: {e}")


async def setup_middlewares():
    """Setup all middlewares"""
    try:
        # Register middlewares
        dp.message.middleware(ThrottlingMiddleware())
        dp.message.middleware(SubscriptionMiddleware(bot))
        dp.callback_query.middleware(BanCallbackMiddleware())
        
        logger.info("Middlewares registered successfully")
    except Exception as e:
        logger.error(f"Error setting up middlewares: {e}")
        raise


async def setup_database():
    """Setup database"""
    try:
        # Initialize and migrate database
        init_db()
        migrate_db()
        logger.info("Database setup completed")
    except Exception as e:
        logger.error(f"Database setup error: {e}")
        raise


async def main():
    """Main application entry point"""
    try:
        logger.info("Starting bot initialization...")
        
        # Setup database
        await setup_database()
        
        # Setup middlewares
        await setup_middlewares()
        
        # Register handlers
        register_handlers(dp)
        
        # Set bot commands
        await set_bot_commands()
        
        logger.info("Bot initialization completed. Starting polling...")
        
        # Start polling
        await dp.start_polling(bot, skip_updates=True)
        
    except asyncio.CancelledError:
        logger.info("Bot polling cancelled")
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        raise
    finally:
        await shutdown()


async def shutdown():
    """Cleanup resources on shutdown"""
    try:
        logger.info("Shutting down bot...")
        
        # Close dispatcher storage
        await dp.storage.close()
        if hasattr(dp.storage, 'wait_closed'):
            await dp.storage.wait_closed()
            
        # Close bot session
        await bot.session.close()
        
        logger.info("Bot shutdown completed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


def handle_signal(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, shutting down...")
    shutdown_event.set()


if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    try:
        # Set event loop policy for Windows
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        # Create and run event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Create main task
        main_task = loop.create_task(main())
        
        # Wait for shutdown signal
        loop.run_until_complete(shutdown_event.wait())
        
        # Cancel main task
        main_task.cancel()
        try:
            loop.run_until_complete(main_task)
        except asyncio.CancelledError:
            pass
        
        # Final cleanup
        loop.run_until_complete(shutdown())
        loop.close()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
    finally:
        logger.info("Application terminated")