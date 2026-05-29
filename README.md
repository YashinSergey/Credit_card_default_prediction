# Credit_card_default_prediction

Проект для прогнозирования дефолта по кредитным картам.  
Датасет: `Default of Credit Card Clients Dataset`.

## Структура проекта

```text
app/
  api.py              # Flask API
  model_handler.py    # загрузка модели и инференс
data/raw/             # исходный датасет
examples/             # примеры запросов к API
models/               # сохраненная модель
notebooks/            # обучение модели
requirements.txt      # зависимости
```

## Локальный запуск API

```bash
pip install -r requirements.txt
python app/api.py
```

Сервис запускается локально на `127.0.0.1:5001`.

Важно: `/predict` вызывается POST-запросом. Если открыть адрес в браузере обычной строкой, браузер отправит GET-запрос, а это не предсказание.

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

## Дополнительно

### ONNX-ML

Модель можно преобразовать в формат ONNX-ML, чтобы запускать инференс не через `scikit-learn`, а через более легкий runtime. Это может ускорить предсказания и упростить перенос модели между разными окружениями. Для этого обычно используют библиотеки `skl2onnx` и `onnxruntime`.

### uWSGI и NGINX

В production Flask-приложение обычно не запускают встроенным сервером.  
uWSGI запускает Python-приложение как стабильный application server, а NGINX стоит перед ним как reverse proxy: принимает внешние HTTP-запросы, отдает статические файлы, управляет таймаутами и передает запросы в uWSGI.
