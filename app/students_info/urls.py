from django.db.models import base
from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('students', views.StudentViewset, basename='student')
router.register('departments', views.DepartmentViewset, basename='department')

urlpatterns = [
    path('', include(router.urls))
]
