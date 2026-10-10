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

- `src/data_loader.py` - загрузка датасета
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

Если датасета нет в папке `data/`, скрипт сам скачает его с Google Drive.
