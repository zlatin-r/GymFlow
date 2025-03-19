from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gym_flow.accounts'

    def ready(self):
        import gym_flow.accounts.signals