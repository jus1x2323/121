import sqlite3
import logging
import json
from typing import List, Optional, Dict, Any
from config.settings import DATABASE_PATH


class DatabaseManager:
    """Database manager for handling all database operations"""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # User management methods
    async def is_user_banned(self, user_id: int) -> bool:
        """Check if user is banned"""
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT 1 FROM banned_users WHERE user_id = ?", (user_id,))
                return cur.fetchone() is not None
        except sqlite3.Error as e:
            logging.error(f"Database error in is_user_banned: {e}")
            return False
    
    def ban_user(self, user_id: int, reason: str, banned_by: int):
        """Ban a user"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT OR REPLACE INTO banned_users (user_id, reason, banned_by) VALUES (?, ?, ?)",
                (user_id, reason, banned_by)
            )
            conn.commit()
    
    def unban_user(self, user_id: int):
        """Unban a user"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
            conn.commit()
    
    # Order management methods
    def create_order(self, order_data: Dict[str, Any]) -> str:
        """Create a new order"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO orders (id, user_id, item, price, username, receipt, game_id, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_data['id'], order_data['user_id'], order_data['item'],
                order_data['price'], order_data.get('username'), order_data.get('receipt'),
                order_data.get('game_id'), order_data.get('status', 'Ожидает проверки')
            ))
            conn.commit()
            return order_data['id']
    
    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get order by ID"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None
    
    def update_order_status(self, order_id: str, status: str):
        """Update order status"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
            conn.commit()
    
    def get_user_orders(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all orders for a user"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]
    
    # Item management methods
    def get_items_by_category(self, table: str, category: str = None) -> List[Dict[str, Any]]:
        """Get items by category"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            if category and table == 'metro_items':
                cur.execute("SELECT * FROM metro_items WHERE category = ?", (category,))
            else:
                cur.execute(f"SELECT * FROM {table}")
            
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def add_item(self, table: str, item_data: Dict[str, Any]) -> int:
        """Add new item to table"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            
            if table == 'metro_items':
                cur.execute("""
                    INSERT INTO metro_items (category, name, price, description, quantity)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    item_data['category'], item_data['name'], item_data['price'],
                    item_data['description'], item_data['quantity']
                ))
            elif table == 'gold_items':
                cur.execute("""
                    INSERT INTO gold_items (name, price, description, quantity)
                    VALUES (?, ?, ?, ?)
                """, (
                    item_data['name'], item_data['price'], 
                    item_data['description'], item_data['quantity']
                ))
            elif table == 'tg_accounts':
                cur.execute("""
                    INSERT INTO tg_accounts (name, price, description, quantity)
                    VALUES (?, ?, ?, ?)
                """, (
                    item_data['name'], item_data['price'],
                    item_data['description'], item_data['quantity']
                ))
            elif table == 'nft_items':
                cur.execute("""
                    INSERT INTO nft_items (name, price, description, gift_link, quantity)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    item_data['name'], item_data['price'], item_data['description'],
                    item_data['gift_link'], item_data['quantity']
                ))
            
            conn.commit()
            return cur.lastrowid
    
    def delete_item(self, table: str, item_id: int):
        """Delete item from table"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {table} WHERE id = ?", (item_id,))
            conn.commit()
    
    def update_item_quantity(self, table: str, item_id: int, quantity: int):
        """Update item quantity"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE {table} SET quantity = ? WHERE id = ?", (quantity, item_id))
            conn.commit()
    
    # Cart management methods
    def get_user_cart(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's cart"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT cart_data FROM carts WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            if row and row[0]:
                try:
                    return json.loads(row[0])
                except json.JSONDecodeError:
                    return []
            return []
    
    def save_user_cart(self, user_id: int, cart_data: List[Dict[str, Any]]):
        """Save user's cart"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cart_json = json.dumps(cart_data)
            cur.execute(
                "INSERT OR REPLACE INTO carts (user_id, cart_data) VALUES (?, ?)",
                (user_id, cart_json)
            )
            conn.commit()
    
    def clear_user_cart(self, user_id: int):
        """Clear user's cart"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM carts WHERE user_id = ?", (user_id,))
            conn.commit()
    
    # Section status management
    def get_section_status(self, section_name: str) -> Dict[str, Any]:
        """Get section status"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT is_open, close_reason FROM section_status WHERE section_name = ?",
                (section_name,)
            )
            row = cur.fetchone()
            if row:
                return {'is_open': bool(row[0]), 'close_reason': row[1]}
            return {'is_open': True, 'close_reason': None}
    
    def update_section_status(self, section_name: str, is_open: bool, reason: str = None):
        """Update section status"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE section_status SET is_open = ?, close_reason = ? WHERE section_name = ?",
                (is_open, reason, section_name)
            )
            conn.commit()
    
    # Notification management
    def add_notification_subscriber(self, user_id: int, section: str):
        """Add notification subscriber"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT OR IGNORE INTO notifications (user_id, section) VALUES (?, ?)",
                (user_id, section)
            )
            conn.commit()
    
    def remove_notification_subscriber(self, user_id: int, section: str):
        """Remove notification subscriber"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM notifications WHERE user_id = ? AND section = ?",
                (user_id, section)
            )
            conn.commit()
    
    def get_notification_subscribers(self, section: str) -> List[int]:
        """Get notification subscribers for section"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT user_id FROM notifications WHERE section = ?", (section,))
            return [row[0] for row in cur.fetchall()]