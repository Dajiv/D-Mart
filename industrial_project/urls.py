
from django.contrib import admin
from django.urls import include, path
from accounts.views import register
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='root_register'),
    path('accounts/', include('accounts.urls')),
    path('', views.home, name='home'),
    
]
