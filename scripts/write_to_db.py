import os
import sys

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

sys.path.append("src")
from data_loader import load_data, fix_types

TABLE_NAME = "kondaurovvv"
N_ROWS = 100


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


if __name__ == "__main__":
    df = fix_types(load_data()).head(N_ROWS)

    engine = get_engine()
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)

    # проверяем что реально записалось
    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT count(*) FROM {TABLE_NAME}")).scalar()
    print("записано строк:", count)
    print(pd.read_sql(f"SELECT * FROM {TABLE_NAME} LIMIT 5", engine).to_string())
