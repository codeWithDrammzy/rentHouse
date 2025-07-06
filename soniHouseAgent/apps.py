from django.apps import AppConfig

class SoniHouseAgentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'soniHouseAgent'

    def ready(self):
        import soniHouseAgent.signals  # Register signals when app is ready
