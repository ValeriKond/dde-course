import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

from .extract import DATA_DIR

PARQUET_PATH = DATA_DIR / "goldapple_products.parquet"


def save_parquet(df, path=PARQUET_PATH):
    df.to_parquet(path, index=False)
    print("сохранено в", path)


def get_engine():
    load_dotenv()
    # через URL.create, а не f-строкой, тк в пароле могут быть спецсимволы
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_URL"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_ROOT_BASE"),
    )
    return create_engine(url)


def load_to_db(df, table):
    engine = get_engine()
    df.to_sql(table, engine, if_exists="replace", index=False)

    # проверяем что реально записалось
    with engine.connect() as conn:
        count = conn.execute(text(f'SELECT count(*) FROM "{table}"')).scalar()
    print("записано строк:", count)
    print(pd.read_sql(f'SELECT * FROM "{table}" LIMIT 5', engine).to_string())
