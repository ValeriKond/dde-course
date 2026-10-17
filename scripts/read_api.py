import os
import time

import pandas as pd
import requests

# архив погоды open-meteo, ключ не нужен
API_URL = "https://archive-api.open-meteo.com/v1/archive"
START_DATE = "2023-01-01"
END_DATE = "2025-12-31"
OUT_PATH = "data/weather_cities.csv"

CITIES = {
    "Москва": (55.75, 37.62),
    "Санкт-Петербург": (59.94, 30.31),
    "Новосибирск": (55.03, 82.92),
    "Екатеринбург": (56.84, 60.61),
    "Казань": (55.79, 49.12),
    "Нижний Новгород": (56.33, 44.00),
    "Самара": (53.20, 50.15),
    "Ростов-на-Дону": (47.23, 39.72),
    "Сочи": (43.59, 39.73),
    "Владивосток": (43.12, 131.89),
}

DAILY = [
    "weather_code", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
    "apparent_temperature_mean", "precipitation_sum", "rain_sum", "snowfall_sum",
    "precipitation_hours", "wind_speed_10m_max", "wind_gusts_10m_max",
    "wind_direction_10m_dominant", "shortwave_radiation_sum", "sunshine_duration",
    "daylight_duration", "sunrise", "sunset",
]


def get_city(city, lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": ",".join(DAILY),
        "timezone": "auto",
    }
    # апи иногда отдает 429 если много качать или просто отваливается по таймауту,
    # тогда ждем и пробуем еще
    for attempt in range(5):
        try:
            resp = requests.get(API_URL, params=params, timeout=120)
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            print("ошибка:", e.__class__.__name__, "жду минуту")
            time.sleep(60)
    else:
        raise RuntimeError(f"не получилось скачать {city}")
    data = resp.json()

    df = pd.DataFrame(data["daily"])
    df.insert(0, "city", city)
    df.insert(1, "elevation", data["elevation"])
    return df


def fix_types(df):
    df = df.rename(columns={"time": "date"})
    df["date"] = pd.to_datetime(df["date"])
    df["sunrise"] = pd.to_datetime(df["sunrise"])
    df["sunset"] = pd.to_datetime(df["sunset"])
    df["city"] = df["city"].astype("category")
    df["weather_code"] = df["weather_code"].astype("Int16")
    df["wind_direction_10m_dominant"] = df["wind_direction_10m_dominant"].astype("Int16")

    # солнце и световой день приходят в секундах, в часах понятнее
    df["sunshine_duration"] = (df["sunshine_duration"] / 3600).round(2)
    df["daylight_duration"] = (df["daylight_duration"] / 3600).round(2)

    float_cols = df.select_dtypes("float64").columns
    df[float_cols] = df[float_cols].astype("float32")
    return df


if __name__ == "__main__":
    parts = []
    for city, (lat, lon) in CITIES.items():
        print("качаю", city)
        parts.append(get_city(city, lat, lon))
        # чтобы не упереться в лимит запросов
        time.sleep(1)

    df = pd.concat(parts, ignore_index=True)
    df = fix_types(df)

    os.makedirs("data", exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    # float32 печатается как 36.700001, так читать удобнее
    pd.set_option("display.float_format", "{:.1f}".format)
    print(df.shape)
    print(df.dtypes)
    print(df.head(15).to_string())
