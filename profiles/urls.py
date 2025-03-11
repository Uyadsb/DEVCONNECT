from rest_framework.routers import DefaultRouter
from .views import ProfileViewSets

router = DefaultRouter()
router.register(r'profiles', ProfileViewSets, basename='profile')

urlpatterns = router.urls
