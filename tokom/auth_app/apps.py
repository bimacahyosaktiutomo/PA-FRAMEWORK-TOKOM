from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_app"

    def ready(self):
        import auth_app.signals  # Import your signals here

        # Connect signal to create groups after migrations are applied
        from django.db.models.signals import post_migrate
        from django.contrib.auth.models import Group
        from django.dispatch import receiver

        @receiver(post_migrate)
        def create_default_groups(sender, **kwargs):
            Group.objects.get_or_create(name='Admin')
            Group.objects.get_or_create(name='Worker')
            Group.objects.get_or_create(name='Customer')
