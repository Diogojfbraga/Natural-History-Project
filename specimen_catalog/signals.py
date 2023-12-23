# specimen_catalog/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Specimen, Expedition

@receiver(post_save, sender=Specimen)
def update_related_models(sender, instance, **kwargs):
    # Get or create an Expedition related to the Specimen
    expedition, created = Expedition.objects.get_or_create(specimen=instance)

    # Update fields in Expedition based on Specimen
    expedition.catalog_number = instance.catalog_number  # Replace with the actual field names
    expedition.save()
