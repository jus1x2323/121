import csv
import logging
from typing import Optional
from database.models import DatabaseManager


async def export_metro_prices() -> Optional[str]:
    """Export metro prices to CSV file"""
    try:
        db = DatabaseManager()
        items = db.get_items_by_category('metro_items')
        
        filename = "metro_prices.csv"
        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Категория', 'Название', 'Цена', 'Количество'])
            
            for item in items:
                writer.writerow([
                    item['category'], 
                    item['name'], 
                    item['price'], 
                    item['quantity']
                ])

        return filename
    except Exception as e:
        logging.error(f"Error exporting metro prices: {e}")
        return None


async def import_metro_prices(csv_text: str) -> bool:
    """Import metro prices from CSV text"""
    try:
        db = DatabaseManager()
        updated_count = 0

        with db.get_connection() as conn:
            cur = conn.cursor()

            for line in csv_text.split('\n'):
                line = line.strip()
                if not line:
                    continue

                try:
                    parts = [part.strip() for part in line.split(';')]
                    if len(parts) != 4:
                        print(f"Пропуск строки: неверный формат - {line}")
                        continue

                    category, name, price, quantity = parts

                    try:
                        price = float(price)
                        quantity = int(quantity)
                    except ValueError as e:
                        print(f"Пропуск строки: неверный формат чисел - {line} ({e})")
                        continue

                    cur.execute("""
                        UPDATE metro_items
                        SET price = ?, quantity = ?
                        WHERE category = ? AND name = ?
                    """, (price, quantity, category, name))

                    if cur.rowcount > 0:
                        updated_count += 1
                        print(f"Успешно обновлено: {category} | {name} | {price} | {quantity}")
                    else:
                        print(f"Не найден товар: {category} | {name}")

                except Exception as e:
                    print(f"Ошибка обработки строки {line}: {e}")
                    continue

            conn.commit()
            print(f"Всего обновлено записей: {updated_count}")

            # Show sample of updated data
            if updated_count > 0:
                cur.execute("SELECT category, name, price, quantity FROM metro_items LIMIT 5")
                sample = cur.fetchall()
                print("Пример данных после обновления:")
                for item in sample:
                    print(item)

            return updated_count > 0

    except Exception as e:
        print(f"Ошибка при импорте: {e}")
        return False