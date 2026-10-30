from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from fiirefly_api.core.views import LivreDorEntryViewSet, SoireeViewSet

router = routers.DefaultRouter()
router.register('soirees', SoireeViewSet)
router.register('livre-dor', LivreDorEntryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
