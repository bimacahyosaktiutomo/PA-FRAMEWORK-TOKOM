from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_app"

    def ready(self):
        import auth_app.signals  # Import your signals here

        # Connect signal to create groups after migrations are applied
        from django.db.models.signals import post_migrate
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from django.dispatch import receiver

        @receiver(post_migrate)
        def create_default_groups(sender, **kwargs):
            # Create groups
            admin_group, _ = Group.objects.get_or_create(name='Admin')
            worker_group, _ = Group.objects.get_or_create(name='Worker')
            customer_group, _ = Group.objects.get_or_create(name='Customer')

            # Define permissions for each group
            admin_permissions = Permission.objects.all()  # Admin gets all permissions
            worker_permissions = Permission.objects.filter(
                content_type__app_label='tokom',
                codename__in=[
                    "add_item",
                    "change_item",
                    "view_item",
                    "add_order",
                    "change_order",
                    "view_order",
                    "view_category",
                ],
            )
            customer_permissions = Permission.objects.filter(
                content_type__app_label='tokom',
                codename__in=[
                    "view_item",
                    "add_order",
                    "view_order",
                    "add_review",
                    "view_review",
                ],
            )

            # Assign permissions to groups
            admin_group.permissions.set(admin_permissions)
            worker_group.permissions.set(worker_permissions)
            customer_group.permissions.set(customer_permissions)
