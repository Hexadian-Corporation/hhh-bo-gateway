from opyoid import Injector

from src.infrastructure.config.dependencies import AppModule, create_injector
from src.infrastructure.config.settings import Settings


def test_create_injector_returns_injector():
    inj = create_injector()
    assert isinstance(inj, Injector)


def test_settings_is_singleton():
    inj = create_injector()
    a = inj.inject(Settings)
    b = inj.inject(Settings)
    assert a is b


def test_app_module_binds_settings():
    inj = Injector([AppModule()])
    settings = inj.inject(Settings)
    assert isinstance(settings, Settings)
    assert settings.port == 8010
