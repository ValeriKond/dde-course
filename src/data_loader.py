import os

import gdown
import pandas as pd

FILE_ID = "1TecBD2z_Ky-DlefZBNW-lCtKOGLzRj5B"
FILE_PATH = "data/goldapple_products.csv"
PARQUET_PATH = "data/goldapple_products.parquet"


def load_data():
    # если файла нет, качаем с гугл диска
    if not os.path.exists(FILE_PATH):
        os.makedirs("data", exist_ok=True)
        gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", FILE_PATH, quiet=False)

    df = pd.read_csv(FILE_PATH)
    return df


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

    cat_cols = ["brand", "category_main", "category_sub", "target_area", "skin_type",
                "target_audience", "application_time", "country"]
    for col in cat_cols:
        df[col] = df[col].astype("category")

    text_cols = ["name", "product_type", "purpose", "active_ingredient", "url"]
    for col in text_cols:
        df[col] = df[col].astype("string")

    return df


def save_parquet(df):
    df.to_parquet(PARQUET_PATH, index=False)
    print("сохранено в", PARQUET_PATH)


if __name__ == "__main__":
    df = load_data()
    df = fix_types(df)
    print(df.dtypes)
    save_parquet(df)
