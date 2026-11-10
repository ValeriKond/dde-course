# DDE course

Проект по курсу "Инжиниринг управления данными". Работаем с датасетом товаров из Золотого Яблока.

## Датасет

Товары из интернет-магазина Золотое Яблоко (уход для лица, тела, волос и тд). Собирал сам с сайта goldapple.ru.

Ссылка на датасет: https://drive.google.com/file/d/1TecBD2z_Ky-DlefZBNW-lCtKOGLzRj5B/view?usp=sharing

- строк: 11992
- столбцов: 20
- формат: csv

### Столбцы

- item_id - артикул
- name - название
- brand - бренд
- product_type - тип продукта
- price_actual - цена со скидкой
- price_regular - цена без скидки
- rating - рейтинг
- reviews_count - кол-во отзывов
- in_stock - есть в наличии или нет
- category_main - категория
- category_sub - подкатегория
- target_area - область применения
- purpose - назначение
- skin_type - тип кожи
- target_audience - для кого
- volume - объем
- application_time - время нанесения
- active_ingredient - активный компонент
- country - страна
- url - ссылка на товар

Есть и числовые и категориальные признаки, есть пропуски, объем записан текстом ("50 мл"), в country есть лишний текст "страна происхождения". Можно потом почистить и например посмотреть от чего зависит цена или рейтинг.

## Структура

```
dde-course/
├── src/
│   └── etl/              - пакет etl (дз8)
│       ├── __init__.py
│       ├── extract.py
│       ├── transform.py
│       ├── validate.py
│       ├── load.py
│       └── main.py
├── scripts/
│   ├── read_api.py       - сбор датасета погоды через API Open-Meteo (дз4), подробнее в scripts/README.md
│   └── screenshot.png
├── notebooks/
│   └── EDA.ipynb         - разведочный анализ, оценка качества данных (дз5, дз6)
├── data/                 - сюда скачивается csv и пишется parquet (в git не попадает)
├── .env.example          - шаблон доступов к БД
├── requirements.txt      - зависимости для etl
└── requirements-dev.txt  - etl + то что нужно для ноутбука и read_api
```

## Пакет etl

Весь цикл от сырого csv до таблицы в БД:

- `extract.py` - если csv нет в `data/`, качает его с Google Drive, потом читает в датафрейм
- `transform.py` - приводит типы колонок (что и как - в разделе "Типы" ниже)
- `validate.py` - проверяет данные после transform: все 20 колонок на месте, item_id и url без пропусков и дублей, цены > 0 и цена со скидкой не больше обычной, рейтинг 1-5, отзывы и объем не отрицательные. Если что-то не так, падает с ошибкой и в БД ничего не пишется
- `load.py` - сохраняет весь датасет в `data/goldapple_products.parquet` и пишет первые N строк в postgres. Если таблица уже есть, она перезаписывается. После записи считает строки в таблице и выводит первые 5
- `main.py` - запускает все по очереди, принимает аргументы

Аргументы `main.py`:

- `--rows` - сколько строк писать в БД, от 1 до 100 (по умолчанию 100)
- `--table` - имя таблицы, только латиница, цифры и _ (по умолчанию `kondaurovvv`)
- `--skip-db` - не писать в БД, только parquet

## Как запустить

1. Склонировать репозиторий

```bash
git clone https://github.com/ValeriKond/dde-course.git
cd dde-course
```

2. Создать виртуальное окружение и активировать его

```bash
python3 -m venv .venv
source .venv/bin/activate
```

На Windows активация через `.venv\Scripts\activate`

3. Установить зависимости

```bash
pip install -r requirements.txt
```

Для ноутбука и `read_api.py` нужны еще dev зависимости: `pip install -r requirements-dev.txt` (туда уже входит requirements.txt)

4. Прописать доступы к БД. Они в репо не лежат, берутся из файла `.env` (он в `.gitignore`)

```bash
cp .env.example .env
```

- `DB_URL` - хост
- `DB_PORT` - порт
- `DB_USER` - пользователь
- `DB_PASSWORD` - пароль
- `DB_ROOT_BASE` - название базы

5. Запустить etl из корня репозитория

```bash
python -m src.etl.main
python -m src.etl.main --rows 50 --table test_table
python -m src.etl.main --skip-db
```

## Типы

- цены в int32, рейтинг в float32, кол-во отзывов в Int32 (там пропуски)
- volume был текстом типо "50 мл", сделал числом (мл)
- в country убрал "страна происхождения" и адреса поставщиков
- бренд, категории, тип кожи, страна и тд в category
- названия, описания, url и item_id в string
