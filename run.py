import os

from server.routers import routers
from vendors.app import Application
from vendors.config import Config
from vendors.router import CustomRoute


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


def run():
    # Подключение конфигурационного файла
    config_path = os.environ.get('CONFIG', 'configs/local.yaml')
    config = Config(file=config_path)

    # Основной объект приложения
    app = Application(config)

    run_server(app=app)


if __name__ == '__main__':
    run()