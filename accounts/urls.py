from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI, RegisterWithPlano
from knox import views as knox_views
from django.conf.urls import url

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    # path('api/auth/active', UsersActiveList.as_view(),name='active-users'),
    path('api/auth/cadastrar-aluno', RegisterWithPlano.as_view(), name='cadastrar'),
   
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),


]
