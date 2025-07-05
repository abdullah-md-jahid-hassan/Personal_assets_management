from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Live reload
    #path('__reload__/', include('django_live_reload.urls')),
    
    # API urls
    path('api/', include('api.urls')),

    # Url for accounts
    path('', include('accounts.urls')),

    # Url for dashboard
    path('dashboard/', include('dashboard.urls')),
]

# URL pattern for media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)