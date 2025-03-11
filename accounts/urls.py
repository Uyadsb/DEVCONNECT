from rest_framework.routers import DefaultRouter
from .views import UserViewsets, SignUpView, LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


Router = DefaultRouter()
Router.register(r'users', UserViewsets, basename='user')

urlpatterns += Router.urls
