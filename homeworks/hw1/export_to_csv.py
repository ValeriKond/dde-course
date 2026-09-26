import json
import csv
from pathlib import Path

def flatten_products(json_path: str, csv_path: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        products = json.load(f)

    # 20 признаков разного типа
    fieldnames = [
        'item_id',
        'name',
        'brand',
        'product_type',
        'price_actual',
        'price_regular',
        'rating',
        'reviews_count',
        'in_stock',
        'category_main',
        'category_sub',
        'target_area',
        'purpose',
        'skin_type',
        'target_audience',
        'volume',
        'application_time',
        'active_ingredient',
        'country',
        'url'
    ]

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for item in products:
            attrs = item.get('product_attrs') or {}
            cats = item.get('categories') or []

            category_main = cats[0] if len(cats) > 0 else ''
            category_sub = cats[1] if len(cats) > 1 else ''

            row = {
                'item_id': item.get('item_id', ''),
                'name': item.get('name', ''),
                'brand': item.get('brand', ''),
                'product_type': item.get('product_type', '') or attrs.get('тип продукта', ''),
                'price_actual': item.get('price_actual'),
                'price_regular': item.get('price_regular'),
                'rating': item.get('rating'),
                'reviews_count': item.get('reviews_count'),
                'in_stock': item.get('in_stock'),
                'category_main': category_main,
                'category_sub': category_sub,
                'target_area': attrs.get('область применения', ''),
                'purpose': attrs.get('назначение', ''),
                'skin_type': attrs.get('тип кожи', ''),
                'target_audience': attrs.get('для кого', ''),
                'volume': attrs.get('объём', ''),
                'application_time': attrs.get('время нанесения', ''),
                'active_ingredient': attrs.get('действующий компонент', ''),
                'country': item.get('manufacturer_info', ''),
                'url': item.get('url', '')
            }
            writer.writerow(row)

    print(f"Готово! Сохранено строк: {len(products)}, признаков: {len(fieldnames)} -> {csv_path}")

if __name__ == '__main__':
    json_file = Path('data/goldapple_products.json')
    csv_file = Path('data/goldapple_products.csv')
    flatten_products(str(json_file), str(csv_file))
