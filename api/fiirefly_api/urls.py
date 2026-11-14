from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from fiirefly_api.core.views import LivreDorEntryViewSet, SoireeViewSet

router = routers.DefaultRouter()
router.register('soirees', SoireeViewSet)
router.register('livre-dor', LivreDorEntryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/', include('fiirefly_api.accounts.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    # en dev django sert les photos, en prod c nginx
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
