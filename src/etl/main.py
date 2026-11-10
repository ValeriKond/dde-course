import argparse
import re

from .extract import load_data
from .load import load_to_db, save_parquet
from .transform import fix_types
from .validate import validate

MAX_ROWS = 100


def parse_args():
    parser = argparse.ArgumentParser(description="ETL датасета товаров Золотого Яблока")
    parser.add_argument("--rows", type=int, default=MAX_ROWS, help="сколько строк писать в БД, не больше 100")
    parser.add_argument("--table", default="kondaurovvv", help="таблица в БД")
    parser.add_argument("--skip-db", action="store_true", help="не писать в БД, только parquet")
    args = parser.parse_args()

    if not 1 <= args.rows <= MAX_ROWS:
        parser.error(f"--rows должен быть от 1 до {MAX_ROWS}")
    # имя таблицы потом идет в sql, поэтому только буквы, цифры и _
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", args.table):
        parser.error("--table: только латиница, цифры и _")
    return args


def main():
    args = parse_args()

    df = load_data()
    df = fix_types(df)
    validate(df)
    save_parquet(df)

    if args.skip_db:
        print("запись в БД пропущена")
    else:
        load_to_db(df.head(args.rows), args.table)


if __name__ == "__main__":
    main()
