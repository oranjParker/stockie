# apps.py
from django.apps import AppConfig


class StockieBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockie_backend'
