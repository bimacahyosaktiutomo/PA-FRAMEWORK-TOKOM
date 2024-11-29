from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from ...models.user_image import UserImage

class Command(BaseCommand):
    help = 'Create UserImage instances for users without one'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Get all users without a UserImage
        users_without_images = User.objects.filter(images__isnull=True)

        for user in users_without_images:
            UserImage.objects.create(user=user)
            self.stdout.write(f'UserImage created for user: {user.username}')

        self.stdout.write(self.style.SUCCESS('All missing UserImage instances have been created!'))
