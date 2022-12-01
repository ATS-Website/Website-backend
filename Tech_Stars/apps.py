from django.apps import AppConfig


class TechStarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Tech_Stars'

    def ready(self):
        import Tech_Stars.signals
