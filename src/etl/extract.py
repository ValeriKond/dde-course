import os
from pathlib import Path

import gdown
import pandas as pd

FILE_ID = "1TecBD2z_Ky-DlefZBNW-lCtKOGLzRj5B"
# пути от корня репо, чтобы запускалось из любой папки
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
FILE_PATH = DATA_DIR / "goldapple_products.csv"


def load_data(path=FILE_PATH):
    # если файла нет, качаем с гугл диска
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", path, quiet=False)

    df = pd.read_csv(path)
    print("загружено", df.shape)
    return df
