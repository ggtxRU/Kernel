<h1 align="center">
  Kernel project
</h1>

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

#### DB для работы сервиса

```bash
CREATE DATABASE kernel_dev;
```

#### DB для тестов

```bash
CREATE DATABASE kernel_test;
```

#### Установка зависимостей

```bash
pip install -r requirements.txt --upgrade pip
```

#### Alembic

```bash
alembic upgrade head && alembic revision --autogenerate -m "Added all" && alembic upgrade head
```


<br>

#### Запуск сервера

```bash
python run.py
```

#### Запуск воркера

```bash
python run.py worker
```

#### Запуск тестов

```bash
pytest
```
