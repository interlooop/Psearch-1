from django.urls import path,register_converter
from . import views,converters

register_converter(converters.EmptyOrSlugConverter, 'emptyorslug')

urlpatterns=[
    path('', views.projects, name="projects"),

    path('project/<str:pk>/', views.singleProject, name="project"),

    path('create-project/', views.createProject, name="create-project"),
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),
    
    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),
    
    path('<emptyorslug:category_slug>/', views.projectsByCategory, name="projects-by-category"),

]