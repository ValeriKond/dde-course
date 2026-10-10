# ДЗ 1

## Датасет

Товары из интернет-магазина Золотое Яблоко (уход для лица, тела, волос и тд). Собирал сам с сайта goldapple.ru.

Ссылка на датасет: https://drive.google.com/file/d/1TecBD2z_Ky-DlefZBNW-lCtKOGLzRj5B/view?usp=sharing

- строк: 11992
- столбцов: 20
- формат: csv

## Столбцы

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
