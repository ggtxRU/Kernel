<h1 align="center">
  Kernel project
</h1>

Сервис для вызова расчета генерации промысловых показателей для нефтянной скважины за указанный период с указанной частотой и хранением результатов.

<br>

## Принцип работы

<pre><h3>FastAPI сервер</h3> -- отвечает на HTTP запросы на порту 3002:<br>


<li><strong>GET /calculations/last</strong> - получить последние запуски расчетов.<br></li>
  <li><strong>GET /calculations/{calculation_id}</strong> - получить конкретный расчет по id.<br></li>
  <li><strong>POST /calculations/create</strong> - создать новый расчет, и поместить его в очередь на выполнение.</li><br></pre>
 
<pre><h3>Абстрактный воркер</h3> -- раз в N секунд забирает из импровизированной очереди задачи на выполнение и сохраняет результат расчета в БД.</pre>

<br>


## Запуск через Docker

```bash
git clone https://github.com/ggtxRU/Kernel.git && cd Kernel && docker-compose up --build
```

<br>

## Запуск без Docker

#### Клонирование репозитория

```bash
git clone https://github.com/ggtxRU/Kernel.git && cd Kernel
```

#### Создать DB для работы сервиса

```bash
CREATE DATABASE kernel_dev;
```

#### Создать DB для тестов

```bash
CREATE DATABASE kernel_test;
```

#### Установка зависимостей

```bash
pip install -r requirements.txt
```

#### Применение миграций

```bash
alembic upgrade head
```


#### Запуск сервера

```bash
python run.py
```

#### Запуск воркера

```bash
python run.py worker
```

<br>

#### Запуск тестов

```bash
pytest
```

#### Увидеть процент покрытия

```bash
open htmlcov/index.html
```
