from rest_framework import serializers

from .models import LivreDorEntry, Membre, Pole, Soiree


class SoireeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soiree
        fields = ['id', 'titre', 'date', 'lieu', 'adresse', 'lien', 'description']


class LivreDorEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LivreDorEntry
        fields = ['id', 'nom', 'message', 'created_at']
        read_only_fields = ['nom', 'created_at']


class PoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pole
        fields = ['id', 'nom', 'couleur', 'ordre']


class MembreSerializer(serializers.ModelSerializer):
    poles = PoleSerializer(many=True, read_only=True)

    class Meta:
        model = Membre
        fields = ['id', 'nom', 'role', 'poles', 'photo', 'description']
