from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User
from .models import Profile

# receiver
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user=instance
        profile=Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        
        subject='Welcome to Search and Colaborate App!'
        message='We are glad you are here!'

        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )
        

@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile=instance
    user=profile.user

    if created==False:
        
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        
        user.save()

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user=instance.user
        user.delete()
    except:
        pass
    


@receiver(post_delete, sender=Profile)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Profile)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    
    try:
        old_img = instance.__class__.objects.get(id=instance.id).profile_image.path
        try:
            new_img = instance.profile_image.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass