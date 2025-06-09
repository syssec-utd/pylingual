from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns
from multiurl import ContinueResolving, multiurl
from django.http import Http404
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from garpix_page.views.sitemap import sitemap_view
from garpix_auth.views import LogoutView, LoginView
from garpix_page.views.page import PageView
from garpix_page.views.index import IndexView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from garpix_page.views.page_api import PageApiView
from garpix_page.views.page_api import PageApiListView
urlpatterns = [path('admin/', admin.site.urls), path('ckeditor/', include('ckeditor_uploader.urls')), path('sitemap.xml', sitemap, sitemap_view(), name='django.contrib.sitemaps.views.sitemap'), re_path(f'{settings.API_URL}/page/(?P<slugs>.*)$', PageApiView.as_view())]
if settings.ENABLE_GARPIX_AUTH:
    urlpatterns += [path('logout/', LogoutView.as_view(url='/'), name='logout'), path('login/', LoginView.as_view(), name='authorize'), path(f'{settings.API_URL}/social-auth/', include('rest_framework_social_oauth2.urls')), path(f'{settings.API_URL}/auth/', include(('garpix_auth.urls', 'garpix_auth'), namespace='garpix_auth')), path(f'{settings.API_URL}/page_models_list/', PageApiListView.as_view())]
if settings.DEBUG:
    urlpatterns += [path(f'{settings.API_URL}/schema/', SpectacularAPIView.as_view(), name='schema'), path(f'{settings.API_URL}/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += i18n_patterns(multiurl(path('', PageView.as_view()), re_path('^(?P<url>.*?)$', PageView.as_view(), name='page'), re_path('^(?P<url>.*?)/$', PageView.as_view(), name='page'), path('', IndexView.as_view()), catch=(Http404, ContinueResolving)), prefix_default_language=settings.USE_DEFAULT_LANGUAGE_PREFIX)