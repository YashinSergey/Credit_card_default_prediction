# Credit_card_default_prediction

Проект для прогнозирования дефолта по кредитным картам.  
Датасет: `Default of Credit Card Clients Dataset`.

## Что реализовано

### Часть 1. Подготовка модели и API

- обучена простая `LogisticRegression`
- модель сохранена в формате `joblib`
- добавлена загрузка модели для инференса
- реализован Flask API с двумя endpoint:
  - `GET /health`
  - `POST /predict`
- формат запроса и ответа описан ниже
- ONNX-ML, uWSGI и NGINX описаны концептуально, без реализации

### Часть 2. Воспроизводимость и Docker

- создан `requirements.txt`
- проект запускается в `.venv`
- создан `Dockerfile`
- образ собирается и запускает API на порту `5001`
- образ опубликован в Docker Hub

### Часть 3. Архитектура и оркестрация

- выбран монолитный подход и описано обоснование
- концепция брокера сообщений описана без реализации
- добавлено JSON-логирование запросов и ответов API
- создан базовый `docker-compose.yml`
- DVC и MLflow описаны концептуально, без реализации
- предложены бизнес-метрики для проекта

### Часть 4. Организация A/B-тестирования

- подготовлен план A/B-теста для сравнения моделей `v1` и `v2`
- описано разделение трафика 50/50
- указана продолжительность теста
- выбраны метрики `F1-score` и `Recall`
- описан bootstrap для доверительного интервала по `F1-score`
- описан критерий успеха теста

## Структура проекта

```text
app/
  api.py              # Flask API
  model_handler.py    # загрузка модели и инференс
data/raw/             # исходный датасет
examples/             # примеры запросов к API
models/               # сохраненная модель
notebooks/            # обучение модели
ARCHITECTURE.md       # архитектурное описание
ab_test_plan.md       # план A/B-тестирования
Dockerfile            # сборка Docker-образа
docker-compose.yml    # запуск сервиса через Docker Compose
requirements.txt      # зависимости
```

## Локальный запуск API

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/api.py
```

Сервис запускается локально на `127.0.0.1:5001`.

Важно: `/predict` вызывается POST-запросом. Если открыть адрес в браузере обычной строкой, браузер отправит GET-запрос, а это не предсказание.

## Запуск в Docker

Опубликованный Docker-образ:

```text
https://hub.docker.com/r/mrblue126/credit-card-default-api
```

Сборка образа:

```bash
docker build -t credit-card-default-api .
```

Запуск контейнера:

```bash
docker run --rm -p 5001:5001 credit-card-default-api
```

Проверка:

```bash
curl http://127.0.0.1:5001/health
```

Запуск опубликованного образа:

```bash
docker pull mrblue126/credit-card-default-api:latest
docker run --rm -p 5001:5001 mrblue126/credit-card-default-api:latest
```

## Запуск через Docker Compose

```bash
docker compose up --build
```

После запуска API доступен на `http://127.0.0.1:5001`.

## Эндпоинты

### GET /health

Проверка работоспособности сервиса.

```bash
curl http://127.0.0.1:5001/health
```

Пример ответа:

```json
{
  "status": "healthy"
}
```

### POST /predict

Принимает JSON с признаками клиента и возвращает прогноз дефолта.

Пример запроса:

```bash
curl -X POST http://127.0.0.1:5001/predict \
  -H "Content-Type: application/json" \
  -d @examples/predict_request.json
```

Файл [examples/predict_request.json](examples/predict_request.json) содержит все признаки клиента, которые использовались при обучении модели.

Пример ответа:

```json
{
  "model_version": "logistic_regression_v1",
  "prediction": 1,
  "probability": 0.66,
  "threshold": 0.42
}
```

`prediction = 1` означает прогноз дефолта, `prediction = 0` означает отсутствие дефолта

## Архитектура и мониторинг

Архитектурные решения, концепция брокера сообщений, логирование, DVC/MLflow и бизнес-метрики описаны в [ARCHITECTURE.md](ARCHITECTURE.md).

## A/B-тестирование

План сравнения текущей модели `v1` и новой модели `v2` описан в [ab_test_plan.md](ab_test_plan.md).

## Дополнительно

### ONNX-ML

Модель можно преобразовать в формат ONNX-ML, чтобы запускать инференс не через `scikit-learn`, а через более легкий runtime. Это может ускорить предсказания и упростить перенос модели между разными окружениями. Для этого обычно используют библиотеки `skl2onnx` и `onnxruntime`.

### uWSGI и NGINX

В production Flask-приложение обычно не запускают встроенным сервером.  
uWSGI запускает Python-приложение как стабильный application server, а NGINX стоит перед ним как reverse proxy: принимает внешние HTTP-запросы, отдает статические файлы, управляет таймаутами и передает запросы в uWSGI.
