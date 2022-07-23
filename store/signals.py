from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Product



@receiver(post_delete, sender=Product)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Product)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass