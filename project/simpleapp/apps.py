from django.apps import AppConfig


class SimpleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleapp'

    def ready(self):  # метод ready, выполнится при завершении конфигурации simpleapp
        from . import signals  # выполнение модуля -> регистрация сигналов
