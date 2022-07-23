from .models import Profile,Skill
from store.models import *

from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


def paginate(request, objects,results):
    
    
    page=request.GET.get('page')
    
    paginator=Paginator(objects, results)

    try:
       objects=paginator.page(page)
    except PageNotAnInteger:
        page=1
        objects=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        objects=paginator.page(page)

    
    leftIndex=(int(page)-4)
    if leftIndex<1:
        leftIndex=1

    rightIndex=(int(page)+5)
    if rightIndex>paginator.num_pages:
        rightIndex=paginator.num_pages+1

    custom_range=range(leftIndex,rightIndex)

    return custom_range, objects


def searchProfiles(request,search_query):

    
    if search_query == None:
        search_query=''
    
    try:
        skillsNames=Skill.objects.filter(name__icontains=search_query).values('name')
    except:
        pass
    
    if search_query ==  '':
        profiles=Profile.objects.all()
    else:
        profiles=Profile.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(intro__icontains=search_query) |
            Q(skill__name__in=skillsNames))

    

    return profiles, search_query
    



class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))


token_generator=TokenGenerator()