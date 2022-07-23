
from django.db import models
import uuid
from django.urls import reverse
from users.models import Profile





class Category(models.Model):
    CATEGORY_VALUE=(
        ('Software Development','development'),
        ('Data Science','datasci') ,
        ('Network Management','network'),
        ('System Administration','sysadm'),
        ('Other','other')
        
    )
    name = models.CharField(max_length=200,choices=CATEGORY_VALUE)
    slug = models.SlugField(max_length=200, unique=True)
    

    class Meta:
        ordering=('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects-by-category', args=[self.slug])




class Project(models.Model):
    
    owner=models.ForeignKey(Profile, null=True,blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image=models.ImageField(null=True, blank=True, upload_to='project-images/',default="project-images/default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tag=models.ManyToManyField('Tag', blank=True)
    total_votes=models.IntegerField(default=0, null=True, blank=True)
    vote_ratio=models.IntegerField(default=0, null=True, blank=True)
    category=models.ForeignKey('Category',related_name='categories' ,blank=False, on_delete=models.CASCADE)
    

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, 
        unique=True, primary_key=True, editable=False)

    def __str__(self): 
        return self.title

    class Meta:
        ordering=['-vote_ratio', '-total_votes','title']

    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url='/images/project-images/default.jpg'
        return url

    @property
    def reviewers(self):
        queryset=self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteStats(self):
        reviews=self.review_set.all()
        upVotes=reviews.filter(value='up').count()
        totalVotes=reviews.count()
        ratio=(upVotes/totalVotes)*100

        self.total_votes=totalVotes
        self.vote_ratio=ratio
        self.save()


class Review(models.Model):
    VOTE_VALUE=(
        ('up', 'Thumb Up'),
        ('down', 'Thumb down')
        
    )
    owner=models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    value=models.CharField(max_length=200, choices=VOTE_VALUE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, 
        unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together=[['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name=models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, 
        unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name

