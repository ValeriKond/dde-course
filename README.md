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

- `src/data_loader.py` - загрузка датасета, приведение типов и сохранение в parquet
- `scripts/read_api.py` - сбор датасета погоды через API Open-Meteo (дз4), подробнее в `scripts/README.md`
- `notebooks/EDA.ipynb` - разведочный анализ датасета, оценка качества данных (дз5)
- `scripts/write_to_db.py` - запись 100 строк датасета в удаленную БД postgres (дз7)
- `data/` - сюда скачивается csv (в git не попадает)

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

4. Запустить скрипт (из корня репозитория)

```bash
python src/data_loader.py
```

Если датасета нет в папке `data/`, скрипт сам скачает его с Google Drive. Потом скрипт приводит типы колонок и сохраняет все в `data/goldapple_products.parquet`, в репо он не попадает.

## Запись в БД

Скрипт `scripts/write_to_db.py` берет первые 100 строк датасета (уже с приведенными типами) и записывает их в таблицу `kondaurovvv` в postgres. Если таблица уже есть, она перезаписывается. После записи скрипт считает строки в таблице и выводит первые 5.

Доступы к БД в репо не лежат, они берутся из файла `.env` (он в `.gitignore`). Чтобы запустить:

1. Скопировать шаблон и вписать туда свои доступы

```bash
cp .env.example .env
```

- `DB_URL` - хост
- `DB_PORT` - порт
- `DB_USER` - пользователь
- `DB_PASSWORD` - пароль
- `DB_ROOT_BASE` - название базы

2. Поставить зависимости (если еще не стоят) и запустить из корня репозитория

```bash
pip install -r requirements.txt
python scripts/write_to_db.py
```

## Типы

- цены в int32, рейтинг в float32, кол-во отзывов в Int32 (там пропуски)
- volume был текстом типо "50 мл", сделал числом (мл)
- в country убрал "страна происхождения" и адреса поставщиков
- бренд, категории, тип кожи, страна и тд в category
- названия, описания, url и item_id в string
