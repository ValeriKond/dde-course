COLUMNS = [
    "item_id", "name", "brand", "product_type", "price_actual", "price_regular",
    "rating", "reviews_count", "in_stock", "category_main", "category_sub",
    "target_area", "purpose", "skin_type", "target_audience", "volume",
    "application_time", "active_ingredient", "country", "url",
]


def validate(df):
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"нет колонок: {sorted(missing)}")

    errors = []
    if df.empty:
        errors.append("датасет пустой")
    if df["item_id"].isna().any() or df["item_id"].duplicated().any():
        errors.append("item_id пустой или повторяется")
    if df["url"].isna().any() or df["url"].duplicated().any():
        errors.append("url пустой или повторяется")
    if (df["price_actual"] <= 0).any() or (df["price_regular"] <= 0).any():
        errors.append("есть цены <= 0")
    if (df["price_actual"] > df["price_regular"]).any():
        errors.append("цена со скидкой больше обычной")
    if not df["rating"].dropna().between(1, 5).all():
        errors.append("рейтинг вне 1-5")
    if (df["reviews_count"].dropna() < 0).any():
        errors.append("отрицательное кол-во отзывов")
    if (df["volume"].dropna() <= 0).any():
        errors.append("объем <= 0")

    if errors:
        raise ValueError("валидация не прошла: " + "; ".join(errors))
    print("валидация ок")
