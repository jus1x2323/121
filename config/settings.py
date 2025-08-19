import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в переменных окружения")

# Database Configuration
DATABASE_PATH = "bot.db"
BACKUP_DIR = "backups"

# Channels and Chat Links
CHANNEL_ID = -1001903841825
ORDER_CHAT_LINK = "https://t.me/+qlXsZ6TmTxE2ZGEy"
DESIGN_CHAT_LINK = "https://t.me/+J3tkaSh623Q0ZWI6"

# Cache Configuration
CACHE_MAX_SIZE = 1000
CACHE_TTL = 900

# Logging Configuration
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"