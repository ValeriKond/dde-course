import pandas as pd

CAT_COLS = ["brand", "category_main", "category_sub", "target_area", "skin_type",
            "target_audience", "application_time", "country"]
TEXT_COLS = ["name", "product_type", "purpose", "active_ingredient", "url"]


def fix_types(df):
    df = df.copy()

    df["item_id"] = df["item_id"].astype("string")
    df["price_actual"] = df["price_actual"].astype("int32")
    df["price_regular"] = df["price_regular"].astype("int32")
    df["rating"] = df["rating"].astype("float32")
    # тут есть пропуски поэтому Int32 а не int32
    df["reviews_count"] = df["reviews_count"].astype("Int32")
    df["in_stock"] = df["in_stock"].astype("bool")

    # объем был текстом "50 мл", оставляем только число
    df["volume"] = df["volume"].str.replace("мл", "").str.replace("л", "").str.strip()
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").astype("float32")

    # в стране лишний текст, иногда еще изготовитель или поставщик с адресом
    df["country"] = df["country"].str.replace("страна происхождения", "")
    df["country"] = df["country"].str.split("изготовитель").str[0]
    df["country"] = df["country"].str.split("поставщик").str[0]
    df["country"] = df["country"].str.strip()
    df.loc[df["country"] == "", "country"] = None

    for col in CAT_COLS:
        df[col] = df[col].astype("category")
    for col in TEXT_COLS:
        df[col] = df[col].astype("string")

    return df
