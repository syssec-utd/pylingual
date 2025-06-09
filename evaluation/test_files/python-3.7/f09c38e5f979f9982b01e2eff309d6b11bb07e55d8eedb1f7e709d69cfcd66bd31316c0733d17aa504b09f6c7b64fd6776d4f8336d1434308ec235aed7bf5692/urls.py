"""Infrastructure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from base_system.views import PermissionsView
from base_system.viewset import group_viewset, permission_viewset, appointment_viewset
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
urlpatterns = [path('register/', views.register), path('login/', obtain_jwt_token), path('token/refresh/', refresh_jwt_token), path('verify/', verify_jwt_token), path('permissions/', PermissionsView.as_view(), name='permissions'), path('change-password/', views.change_password), path('all-permissions/', group_viewset.all_permissions), path('own-menu/', group_viewset.get_own_permissions), path('import_position_title/', views.import_position_title), path('import_office/', views.import_office), path('import_doctor/', views.import_doctor), path('menu_permissions/', permission_viewset.menu_permissions)]
router = routers.DefaultRouter()
router.register('export_hospital', views.HospitalInfoExportViewSet)
router.register('export_office', views.OfficeInfoExportViewSet)
router.register('export_group', views.GroupExportViewSet)
router.register('export_doctor', views.DoctorInfoExportViewSet)
router.register('export_user', views.UserInfoExportViewSet)
router.register('groups', group_viewset.GroupViewSet)
router.register('users', views.UserViewSet)
router.register('ins_dic', views.InspectionDictionariesViewSet)
router.register('export_ins_dic', views.InspectionDictionariesInfoExportViewSet)
router.register('exa_dic', views.ExaminationDictionariesViewSet)
router.register('export_exa_dic', views.ExaminationDictionariesInfoExportViewSet)
router.register('export_drug_directory', views.DrugDirectoryExportViewSet)
router.register('pharmacy_management', views.PharmacyManagementViewSet)
router.register('hospitals', appointment_viewset.HospitalViewSet)
router.register('offices', appointment_viewset.OfficeViewSet)
router.register('doctors', appointment_viewset.DoctorViewSet)
urlpatterns += router.urls