from django.contrib import admin
from django.utils.html import format_html

from .models import LivreDorEntry, Membre, Pole, Soiree


@admin.register(Soiree)
class SoireeAdmin(admin.ModelAdmin):
    list_display = ['titre', 'date', 'lieu']
    search_fields = ['titre', 'lieu']
    date_hierarchy = 'date'


@admin.register(LivreDorEntry)
class LivreDorEntryAdmin(admin.ModelAdmin):
    list_display = ['nom', 'auteur', 'message', 'created_at', 'is_visible']
    list_editable = ['is_visible']
    list_filter = ['is_visible', 'auteur']
    search_fields = ['nom', 'message', 'auteur__username']
    actions = ['approve', 'hide']

    @admin.action(description='Rendre visibles')
    def approve(self, request, queryset):
        queryset.update(is_visible=True)

    @admin.action(description='Masquer')
    def hide(self, request, queryset):
        queryset.update(is_visible=False)


@admin.register(Pole)
class PoleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pastille', 'couleur', 'ordre']
    list_editable = ['couleur', 'ordre']

    @admin.display(description='')
    def pastille(self, obj):
        return format_html(
            '<span style="display:inline-block;width:1em;height:1em;border-radius:50%;'
            'background:{}"></span>',
            obj.couleur,
        )


@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ['photo_preview', 'nom', 'role', 'poles_display', 'ordre', 'is_visible']
    list_display_links = ['photo_preview', 'nom']
    list_editable = ['ordre', 'is_visible']
    list_filter = ['poles', 'is_visible']
    search_fields = ['nom', 'role']
    readonly_fields = ['photo_preview']
    filter_horizontal = ['poles']
    fields = [
        'nom',
        'role',
        'poles',
        'photo',
        'photo_preview',
        'description',
        'ordre',
        'is_visible',
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('poles')

    @admin.display(description='Pôles')
    def poles_display(self, obj):
        return ', '.join(p.nom for p in obj.poles.all()) or '-'

    @admin.display(description='Photo')
    def photo_preview(self, obj):
        if not obj.photo:
            return '-'
        return format_html(
            '<img src="{}" style="width:64px;height:64px;border-radius:50%">', obj.photo.url
        )
