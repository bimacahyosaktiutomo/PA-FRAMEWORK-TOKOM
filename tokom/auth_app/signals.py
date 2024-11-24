from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

@receiver(post_save, sender=User)
def add_to_customer_group(sender, instance, created, **kwargs):
    if created:
        customer_group = Group.objects.get(name='Customer')
        instance.groups.add(customer_group)