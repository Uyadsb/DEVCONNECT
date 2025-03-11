
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('a/', admin.site.urls),
    path('ip/', include('profiles.urls')),
    # path('api/', include('skills.urls')),
    path('i/', include('accounts.urls')),    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)