import os

import gdown
import pandas as pd

FILE_ID = "1TecBD2z_Ky-DlefZBNW-lCtKOGLzRj5B"
FILE_PATH = "data/goldapple_products.csv"


def load_data(path=FILE_PATH):
    # если файла нет, качаем с гугл диска
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", path, quiet=False)

    df = pd.read_csv(path)
    print("загружено", df.shape)
    return df
