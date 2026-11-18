from django.urls import path

from .views import (LoginView, LogoutView, ProfilView, SetPinView)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profil/', ProfilView.as_view(), name='profil'),
    path('set-pin/', SetPinView.as_view(), name='set-pin'),
]
