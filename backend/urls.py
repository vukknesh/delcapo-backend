from django.contrib import admin
from django.conf.urls import url, include as inc
from django.urls import path, include
urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('userprofile.urls')),

    url(r'^api/pizza/', inc(("pizza.urls", 'pizza'),
                            namespace='pizza-api')),
]
