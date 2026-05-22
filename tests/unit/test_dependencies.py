from opyoid import Injector

from src.infrastructure.config.dependencies import AppModule
from src.infrastructure.config.settings import Settings


def test_app_module_binds_settings_singleton():
    settings = Settings()
    injector = Injector(modules=[AppModule(settings)])
    assert injector.inject(Settings) is settings
