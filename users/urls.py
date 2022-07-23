from django.urls import path
from . import views
from .views import *

# app_name='users'

urlpatterns =[

    path('login/', LoginUserView.as_view(), name="login-user"),
    path('logout/', LogoutUserView.as_view(), name="logout-user"),
    
    path('register/', RegisterUserView.as_view(), name="register-user"),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name="activate"),
    path('activation-successful/', ActivationSuccessfulView.as_view(), name="activation-successful"),
    
    path('', ProfilesView.as_view(), name="profiles"),
    
    path('user/<str:pk>/', UserProfileView.as_view(), name="user-profile"),
    path('account/', UserAccountView.as_view(), name="account"),
    path('account/paginated-user-projects/', PaginatedUserProjectsView.as_view(), name="paginated-user-projects"),
    path('edit-account/', EditAccountView.as_view(), name="edit-account"),

    
    path('create-skill/', CreateSkillView.as_view(), name="create-skill"),
    path('update-skill/<str:pk>/', UpdateSkillView.as_view(), name="update-skill"),
    path('delete-skill/<str:pk>/', DeleteSkillView.as_view(), name="delete-skill"),

    
    path('inbox/', InboxView.as_view(), name="inbox"),
    path('message/<str:pk>/', ViewMessageView.as_view(), name="view-message"),
    path('inbox/paginated-inbox/', PaginatedInboxView.as_view(), name="paginated-inbox"),
    path('create-message/<str:pk>', CreateMessageView.as_view(), name="create-message"),
    path('delete-message/<str:pk>/', DeleteMessageView.as_view(), name="delete-message"),

    path('filtered-profiles/', FilteredProfilesView.as_view(), name="filtered-profiles"),

]