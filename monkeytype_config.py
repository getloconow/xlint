import os
from monkeytype.config import DefaultConfig, contextmanager
from typing import Generator


os.environ['DJANGO_SETTINGS_MODULE'] = 'questions.settings'


class MyConfig(DefaultConfig):
    @contextmanager
    def cli_context(self: 'MyConfig', command: str) -> Generator:
        import django
        django.setup()
        yield


CONFIG = MyConfig()
