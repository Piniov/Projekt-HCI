from django.conf.urls import url
from django.contrib import admin

from myproject.weather_forecast import views


urlpatterns = [
    url('^$', views.home, name='home'),
    url('forecast/', views.forecast, name='forecast'),
    url('about/', views.about, name='about'),
    url('admin/', admin.site.urls),
]
