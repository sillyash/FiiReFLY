from django.db.models import F, Min
from rest_framework import mixins, permissions, viewsets
from rest_framework.throttling import ScopedRateThrottle

from fiirefly_api.accounts.arise import display_name

from .models import LivreDorEntry, Membre, Soiree
from .serializers import LivreDorEntrySerializer, MembreSerializer, SoireeSerializer


class SoireeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Soiree.objects.all()
    serializer_class = SoireeSerializer


class LivreDorEntryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    # les messages masqués depuis l'admin sont pas exposés
    queryset = LivreDorEntry.objects.filter(is_visible=True)
    serializer_class = LivreDorEntrySerializer
    throttle_scope = 'livre-dor'

    def get_permissions(self):
        # lire = tout le monde, poster = connecté via arise
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_throttles(self):
        # throttle seulement sur le POST, pas sur la lecture
        if self.action == 'create':
            return [ScopedRateThrottle()]
        return []

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(auteur=user, nom=display_name(user)[:50])


class MembreViewSet(viewsets.ReadOnlyModelViewSet):
    # trié par le pole principal (ordre le plus petit), les sans pole a la fin
    queryset = (
        Membre.objects.filter(is_visible=True)
        .annotate(pole_ordre=Min('poles__ordre'))
        .order_by(F('pole_ordre').asc(nulls_last=True), 'ordre', 'nom')
        .prefetch_related('poles')
    )
    serializer_class = MembreSerializer
    # le trombi affiche tout le monde d'un coup
    pagination_class = None
