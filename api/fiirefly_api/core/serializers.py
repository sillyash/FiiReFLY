from rest_framework import serializers

from .models import LivreDorEntry, Membre, Pole, Soiree


class SoireeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soiree
        fields = ['id', 'titre', 'date', 'lieu', 'adresse', 'lien', 'description']


class LivreDorEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LivreDorEntry
        fields = ['id', 'nom', 'message', 'created_at', 'updated_at']
        read_only_fields = ['nom', 'created_at', 'updated_at']


class LivreDorMoiSerializer(LivreDorEntrySerializer):
    # pour son propre message on dit aussi s'il est masqué par la modo
    class Meta(LivreDorEntrySerializer.Meta):
        fields = LivreDorEntrySerializer.Meta.fields + ['is_visible']
        read_only_fields = LivreDorEntrySerializer.Meta.read_only_fields + ['is_visible']


class PoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pole
        fields = ['id', 'nom', 'couleur', 'ordre']


class MembreSerializer(serializers.ModelSerializer):
    poles = PoleSerializer(many=True, read_only=True)

    class Meta:
        model = Membre
        fields = ['id', 'nom', 'role', 'poles', 'photo', 'description']
