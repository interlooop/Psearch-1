from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    EXPERIENCE_VALUE=(
        ('0-2 years', '0-2 years'),
        ('2-4 years', '2-4 years'),
        ('4+ years', '4+ years')
        
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(max_length=500, null=True,blank=True)
    username=models.CharField(max_length=200,null=True,blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    intro=models.CharField(max_length=200,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    experience=models.CharField(max_length=200, choices=EXPERIENCE_VALUE,default="0-2 years")
    profile_image=models.ImageField(null=True, blank=True, upload_to='profile-images/', default='profile-images/user-default.png')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, 
        unique=True, primary_key=True, editable=False)


    def __str__(self):
        return str(self.username)


    class Meta:
        ordering=['created']

    
    @property
    def imageUrl(self):
        try:
            url=self.profile_image.url
        except:
            url='/images/profile-images/user-default.png'
        return url


class Social(models.Model):
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
    social_github=models.CharField(max_length=200,null=True,blank=True)
    social_twitter=models.CharField(max_length=200,null=True,blank=True)
    social_linkedin=models.CharField(max_length=200,null=True,blank=True)
    social_website=models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, 
        unique=True, primary_key=True, editable=False)


    def __str__(self):
        return str(self.owner)

        
class Skill(models.Model):
    owner=models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200, null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, 
        unique=True, primary_key=True, editable=False)


    def __str__(self):
        return str(self.name)



class Message(models.Model):
    sender=models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True,blank=True)
    recipient=models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True, related_name="messages")
    name=models.CharField(max_length=200,null=False,blank=False)
    email=models.EmailField(max_length=500,null=True,blank=True)
    subject=models.CharField(max_length=200,blank=True)
    body=models.TextField()
    is_read=models.BooleanField(default=False,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, 
        unique=True, primary_key=True, editable=False)


    def __str__(self):
        if self.subject:
            return self.subject
        else:
            return self.name

    class Meta:
        ordering=['is_read','-created']


