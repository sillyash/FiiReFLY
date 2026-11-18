from django.db import IntegrityError, transaction
from django.db.models import F, Min
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from fiirefly_api.accounts.arise import display_name

from .models import LivreDorEntry, Membre, Soiree
from .serializers import (
    LivreDorEntrySerializer,
    LivreDorMoiSerializer,
    MembreSerializer,
    SoireeSerializer,
)

DEJA_SIGNE = "Tu as déjà signé le livre d'or, modifie ton message à la place."


class SoireeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Soiree.objects.all()
    serializer_class = SoireeSerializer


class LivreDorEntryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    # les messages masqués depuis l'admin sont pas exposés
    queryset = LivreDorEntry.objects.filter(is_visible=True)
    serializer_class = LivreDorEntrySerializer
    throttle_scope = 'livre-dor'

    def get_serializer_class(self):
        # au POST on renvoie aussi is_visible, le front s'en sert comme "mon message"
        if self.action == 'create':
            return LivreDorMoiSerializer
        return LivreDorEntrySerializer

    def get_permissions(self):
        # lire = tout le monde, poster/modifier = connecté via arise
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_throttles(self):
        # throttle sur le POST et l'edit, pas sur la lecture ni le delete
        if self.action == 'create' or (self.action == 'moi' and self.request.method == 'PATCH'):
            return [ScopedRateThrottle()]
        return []

    def perform_create(self, serializer):
        user = self.request.user
        # meme un message masqué compte, sinon on contourne la modo en reposant
        if LivreDorEntry.objects.filter(auteur=user).exists():
            raise ValidationError({'message': [DEJA_SIGNE]})
        try:
            with transaction.atomic():
                serializer.save(auteur=user, nom=display_name(user)[:50])
        except IntegrityError:
            # double clic, la contrainte en base a bloqué le 2eme
            raise ValidationError({'message': [DEJA_SIGNE]}) from None

    @action(detail=False, methods=['get', 'patch', 'delete'], url_path='moi')
    def moi(self, request):
        # pas self.queryset, il filtre is_visible et on veut voir son message masqué
        entry = get_object_or_404(LivreDorEntry, auteur=request.user)

        if request.method == 'DELETE':
            entry.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == 'PATCH':
            serializer = LivreDorMoiSerializer(entry, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(nom=display_name(request.user)[:50])
            return Response(serializer.data)

        return Response(LivreDorMoiSerializer(entry).data)


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
