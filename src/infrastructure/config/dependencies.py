from opyoid import Module, SingletonScope

from src.infrastructure.config.settings import Settings


class AppModule(Module):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self._settings = settings

    def configure(self) -> None:
        self.bind(Settings, to_instance=self._settings, scope=SingletonScope)
