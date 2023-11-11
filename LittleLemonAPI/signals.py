from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import *

@receiver(pre_save, sender=Cart)
def set_unit_price_from_menuitem(sender, instance, **kwargs):
    instance.unit_price = instance.menuitem.price

@receiver(pre_save, sender=Cart)
def set_unit_price_from_menuitem(sender, instance, **kwargs):
    instance.unit_price = instance.menuitem.price
    instance.price = instance.unit_price * instance.quantity

@receiver(pre_save, sender=OrderItem)
def set_unit_price_from_menuitem(sender, instance, **kwargs):
    instance.unit_price = instance.menuitem.price

@receiver(pre_save, sender=OrderItem)
def set_unit_price_from_menuitem(sender, instance, **kwargs):
    instance.unit_price = instance.menuitem.price
    instance.price = instance.unit_price * instance.quantity