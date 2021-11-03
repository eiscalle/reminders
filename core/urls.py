
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.urls import path, include
from django.views.generic import TemplateView

from reminders import urls as reminders_urls
from users import urls as users_urls

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include(auth_urls)),
    path('users/', include(users_urls)),
    path('reminders/', include(reminders_urls)),
]
