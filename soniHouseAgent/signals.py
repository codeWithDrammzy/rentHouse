from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Tenant

@receiver(post_delete, sender=Tenant)
def make_house_available(sender, instance, **kwargs):
    house = instance.house
    house.is_available = True
    house.save()
    print(f"House '{house}' is now marked as available after tenant deletion.")
