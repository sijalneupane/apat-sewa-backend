from django.urls import path
from . import views
from .views import VolunterCreateView, VolunterListView


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
     path('update/', views.UserUpdateView.as_view(), name='user-update'),
      path('volunteers/', VolunterListView.as_view(), name='volunteer-list'),
    path('volunteers/create/', VolunterCreateView.as_view(), name='volunteer-create'),
]