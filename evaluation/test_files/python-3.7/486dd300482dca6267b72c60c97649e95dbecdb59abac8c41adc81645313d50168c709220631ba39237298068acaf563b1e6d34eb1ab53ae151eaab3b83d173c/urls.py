from django.urls import re_path
from binary_database_files import views
urlpatterns = [re_path('^files/(?P<name>.+)$', views.serve_mixed, name='database_file')]