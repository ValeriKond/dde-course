# DDE course

Домашки по курсу "Инжиниринг управления данными".

- `homeworks/hw1` - датасет
- `homeworks/hw2` - загрузка датасета

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
python homeworks/hw2/data_loader.py
```

Если датасета нет в папке `data/`, скрипт сам скачает его с Google Drive.
