import sqlite3
import logging
import shutil
import os
from datetime import datetime
from typing import Optional
from config.settings import DATABASE_PATH, BACKUP_DIR
from config.constants import SECTIONS, METRO_ITEMS_DATA


def backup_db() -> str:
    """Create a backup of the database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{BACKUP_DIR}/bot_db_{timestamp}.db"
    os.makedirs(BACKUP_DIR, exist_ok=True)
    shutil.copy(DATABASE_PATH, backup_path)
    logging.info(f"DB backed up: {backup_path}")
    return backup_path


def migrate_db():
    """Apply database migrations"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cur = conn.cursor()
            
            # Check and add missing columns
            try:
                cur.execute("SELECT game_id FROM orders LIMIT 1")
            except sqlite3.OperationalError:
                cur.execute("ALTER TABLE orders ADD COLUMN game_id TEXT")

            # Add quantity column to item tables
            tables = ["gold_items", "tg_accounts", "nft_items", "metro_items"]
            for table in tables:
                try:
                    cur.execute(f"SELECT quantity FROM {table} LIMIT 1")
                except sqlite3.OperationalError:
                    cur.execute(f"ALTER TABLE {table} ADD COLUMN quantity INTEGER DEFAULT 1")

            # Ensure metro_items table exists
            cur.execute('''CREATE TABLE IF NOT EXISTS metro_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                name TEXT,
                price REAL,
                description TEXT,
                quantity INTEGER DEFAULT 1
            )''')
            
            conn.commit()
            logging.info("Database migrations completed successfully")
            
    except sqlite3.Error as e:
        logging.error(f"Database migration error: {e}")
        raise


def init_db():
    """Initialize the database with all required tables"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cur = conn.cursor()
            
            # Create all tables
            tables = [
                '''CREATE TABLE IF NOT EXISTS item_reservations(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    order_id TEXT,
                    expires_at TIMESTAMP NOT NULL
                )''',
                
                '''CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    item TEXT,
                    price REAL,
                    username TEXT,
                    receipt TEXT,
                    game_id TEXT,
                    status TEXT DEFAULT 'Ожидает проверки',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''',
                
                '''CREATE TABLE IF NOT EXISTS requests (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    user_contact TEXT,
                    text TEXT,
                    media_type TEXT,
                    media_id TEXT,
                    status TEXT DEFAULT 'В обработке',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''',
                
                '''CREATE TABLE IF NOT EXISTS banned_users (
                    user_id INTEGER PRIMARY KEY,
                    reason TEXT,
                    banned_by INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''',
                
                '''CREATE TABLE IF NOT EXISTS section_status (
                    section_name TEXT PRIMARY KEY,
                    is_open INTEGER DEFAULT 1,
                    close_reason TEXT
                )''',
                
                '''CREATE TABLE IF NOT EXISTS gold_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price REAL,
                    description TEXT,
                    quantity INTEGER DEFAULT 1
                )''',
                
                '''CREATE TABLE IF NOT EXISTS tg_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price REAL,
                    description TEXT,
                    quantity INTEGER DEFAULT 1
                )''',
                
                '''CREATE TABLE IF NOT EXISTS nft_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price REAL,
                    description TEXT,
                    gift_link TEXT,
                    quantity INTEGER DEFAULT 1
                )''',
                
                '''CREATE TABLE IF NOT EXISTS metro_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    name TEXT,
                    price REAL,
                    description TEXT,
                    quantity INTEGER DEFAULT 1
                )''',
                
                '''CREATE TABLE IF NOT EXISTS carts (
                    user_id INTEGER PRIMARY KEY,
                    cart_data TEXT
                )''',
                
                '''CREATE TABLE IF NOT EXISTS profile_design_requests (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    video_id TEXT,
                    status TEXT DEFAULT 'На модерации',
                    account_class TEXT,
                    price REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''',
                
                '''CREATE TABLE IF NOT EXISTS notifications (
                    user_id INTEGER,
                    section TEXT,
                    PRIMARY KEY(user_id, section)
                )'''
            ]

            for table_sql in tables:
                cur.execute(table_sql)

            # Initialize sections
            for section in SECTIONS:
                cur.execute(
                    "INSERT OR IGNORE INTO section_status (section_name) VALUES (?)", 
                    (section,)
                )

            # Initialize metro items if empty
            cur.execute("SELECT COUNT(*) FROM metro_items")
            if cur.fetchone()[0] == 0:
                cur.executemany(
                    "INSERT INTO metro_items (category, name, price, description, quantity) VALUES (?, ?, ?, ?, ?)",
                    METRO_ITEMS_DATA
                )

            conn.commit()
            logging.info("Database initialized successfully")
            
    except sqlite3.Error as e:
        logging.error(f"Database initialization error: {e}")
        raise


def get_connection() -> sqlite3.Connection:
    """Get a database connection"""
    return sqlite3.connect(DATABASE_PATH)