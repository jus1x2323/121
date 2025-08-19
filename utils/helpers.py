import random
import json
import logging
from typing import List, Dict, Any
from database.models import DatabaseManager


def generate_id(prefix: str) -> str:
    """Generate a random ID with prefix"""
    return f"{prefix}-{random.randint(100000, 999999)}"


async def remove_item_from_all_carts(item_name: str, bot) -> None:
    """Remove item from all user carts when it's out of stock"""
    db = DatabaseManager()
    
    try:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT user_id, cart_data FROM carts")
            carts = cur.fetchall()
            
            for user_id, cart_json in carts:
                if not cart_json:
                    continue
                    
                try:
                    cart = json.loads(cart_json)
                    new_cart = [item for item in cart if item['name'] != item_name]
                    
                    if len(cart) != len(new_cart):
                        new_cart_json = json.dumps(new_cart)
                        cur.execute(
                            "UPDATE carts SET cart_data = ? WHERE user_id = ?", 
                            (new_cart_json, user_id)
                        )
                        
                        # Notify user
                        try:
                            await bot.send_message(
                                user_id,
                                f"⚠️ Товар '{item_name}' закончился и был удален из вашей корзины.",
                                parse_mode="HTML"
                            )
                        except Exception:
                            # User might have blocked the bot
                            pass
                            
                except json.JSONDecodeError:
                    continue
            
            conn.commit()
            
    except Exception as e:
        logging.error(f"Error removing item from carts: {e}")


def format_price(price: float) -> str:
    """Format price with currency symbol"""
    return f"{price} ₽"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."