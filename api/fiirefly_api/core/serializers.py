from rest_framework import serializers

from .models import LivreDorEntry, Soiree


class SoireeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soiree
        fields = ['id', 'titre', 'date', 'lieu', 'adresse', 'lien', 'description']


class LivreDorEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LivreDorEntry
        fields = ['id', 'nom', 'message', 'created_at']
        read_only_fields = ['created_at']
