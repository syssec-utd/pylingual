from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'photofolio'
urlpatterns = [path('robots.txt', views.robots), path('', views.home, name='home'), path('about/', views.about, name='about'), path('contact/', views.contact, name='contact'), path('gallery/<str:category>/', views.gallery, name='gallery'), path('services/', views.services, name='services')]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)