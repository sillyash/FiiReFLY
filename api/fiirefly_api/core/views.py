from rest_framework import mixins, permissions, viewsets
from rest_framework.throttling import ScopedRateThrottle

from .models import LivreDorEntry, Soiree
from .serializers import LivreDorEntrySerializer, SoireeSerializer


class SoireeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Soiree.objects.all()
    serializer_class = SoireeSerializer


class LivreDorEntryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = LivreDorEntry.objects.all()
    serializer_class = LivreDorEntrySerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'livre-dor'
