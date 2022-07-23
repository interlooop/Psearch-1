from django.urls import path

from . import views

app_name='cart'

urlpatterns=[
    path('', views.cart_summaryView.as_view(), name='cart-summary'),
    path('add/', views.cart_addView.as_view(),  name='cart-add'),
    path('delete/', views.cart_deleteView.as_view(),  name='cart-delete'),
    path('update/', views.cart_updateView.as_view(),  name='cart-update')
]
