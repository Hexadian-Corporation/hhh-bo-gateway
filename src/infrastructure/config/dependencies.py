from opyoid import Injector, Module, SingletonScope

from src.infrastructure.config.settings import Settings


class AppModule(Module):
    def configure(self) -> None:
        self.bind(Settings, to_instance=Settings(), scope=SingletonScope)


def create_injector() -> Injector:
    return Injector([AppModule()])
