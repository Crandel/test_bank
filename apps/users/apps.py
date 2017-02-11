from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"
    verbose_name = "Users Application"

    def ready(self):
        import users.signals
