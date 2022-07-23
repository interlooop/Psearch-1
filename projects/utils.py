
from .models import Project,Tag
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from store.models import *



def paginateProjects(request, projects,results):
    
    
    page=request.GET.get('page')
    
    paginator=Paginator(projects, results)

    try:
       projects=paginator.page(page)
    except PageNotAnInteger:
        page=1
        projects=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        projects=paginator.page(page)

    
    leftIndex=(int(page)-4)
    if leftIndex<1:
        leftIndex=1

    rightIndex=(int(page)+5)
    if rightIndex>paginator.num_pages:
        rightIndex=paginator.num_pages+1

    custom_range=range(leftIndex,rightIndex)

    return custom_range, projects



def searchProjects(request,search_query,category=None):

    if search_query == None:
        search_query=''


    tags=Tag.objects.filter(name__icontains=search_query)

    if category:
        projects=Project.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(owner__name__icontains=search_query) |
            Q(tag__in=tags),
            category=category
        )
    else:
        projects=Project.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(owner__name__icontains=search_query) |
            Q(tag__in=tags)
            
        )

    return projects,search_query