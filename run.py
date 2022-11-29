import argparse
import asyncio
import os
import sys
from enum import Enum

from server.routers import routers
from vendors.app import Application
from vendors.config import Config
from vendors.router import CustomRoute
from vendors.services.calculation_process_worker import CalculationProcessWorkerService


class DriverEnum(str, Enum):
    server = 'server'
    worker = 'worker'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('driver', nargs='?')
    return parser.parse_args(sys.argv[1:])


def run_server(app: Application):
    # Инициализация объекта сервера приложения FastAPI
    app.init_fast_api_server()

    # Создание и проверка подключения к основной базе данных
    app.init_primary_database_for_server()

    # Инициализация кастомного роутера
    CustomRoute.set_app(app)

    # Подключение роутеров
    app.add_routers(routers)

    # Запуск сервера приложения
    app.run_server()


def run_service_for_generating_field_indicators(app: Application):
    # Создание и проверка подключения к основной базе данных
    app.init_async_primary_database()

    # Запуск воркера
    service = CalculationProcessWorkerService(app)
    asyncio.run(service.run())


def run():
    # Подключение конфигурационного файла
    config_path = os.environ.get('CONFIG', 'configs/local.yaml')
    config = Config(file=config_path)

    # Основной объект приложения
    app = Application(config)

    # Чтение аргументов командной строки и запуск сервиса
    args = get_args()
    if not args.driver or args.driver == DriverEnum.server:
        run_server(app=app)
    elif args.driver == DriverEnum.worker:
        run_service_for_generating_field_indicators(app=app)


if __name__ == '__main__':
    run()
