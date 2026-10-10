import os

import gdown
import pandas as pd

FILE_ID = "1TecBD2z_Ky-DlefZBNW-lCtKOGLzRj5B"
FILE_PATH = "data/goldapple_products.csv"


def load_data():
    # если файла нет, качаем с гугл диска
    if not os.path.exists(FILE_PATH):
        os.makedirs("data", exist_ok=True)
        gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", FILE_PATH, quiet=False)

    df = pd.read_csv(FILE_PATH)
    print(df.head(10))
    return df


if __name__ == "__main__":
    load_data()
