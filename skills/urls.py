from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillViewSets

router = DefaultRouter()
router.register(r'skills', SkillViewSets, basename='skills')

urlpatterns = router.urls