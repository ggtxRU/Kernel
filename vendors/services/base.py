import time
from abc import ABC, abstractmethod
from typing import Callable

from vendors.app import Application


class BaseService(ABC):

    def __init__(self, app: Application) -> None:
        self.__app = app

    def get_app(self) -> Application:
        return self.__app

    @property
    @abstractmethod
    def service_name(self) -> str:
        pass

    @property
    @abstractmethod
    def purpose_func(self) -> Callable:
        pass

    @property
    @abstractmethod
    def time_sleep(self) -> int:
        pass

    async def run(self) -> None:
        print(f'{self.service_name} start working!')
        while True:
            session = self.get_app().create_async_session()
            try:
                await self.purpose_func(session=session)
                await session.commit()
                time.sleep(self.time_sleep)
            except BaseException as exc:
                print(exc)
                await self.get_app().close_async_primary_database()
                print(f'{self.service_name} stop working!')
                break
            finally:
                await session.close()
