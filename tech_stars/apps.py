from django.apps import AppConfig


class TechStarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tech_stars'

    def ready(self) -> None:
        import tech_stars.signals
