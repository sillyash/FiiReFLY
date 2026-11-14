from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from fiirefly_api.core.roles import LISTE_GROUP

from .models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


admin.site.unregister(User)


@admin.register(User)
class AriseUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'profile__nickname', 'in_liste', 'is_staff']
    list_filter = ['groups', 'is_staff', 'is_superuser']
    search_fields = ['username', 'profile__nickname']
    actions = ['add_to_liste', 'remove_from_liste']

    @admin.display(description='Liste', boolean=True)
    def in_liste(self, obj):
        return obj.groups.filter(name=LISTE_GROUP).exists()

    @admin.action(description='Ajouter à la liste')
    def add_to_liste(self, request, queryset):
        group = Group.objects.get(name=LISTE_GROUP)
        for user in queryset:
            user.groups.add(group)
        # is_staff sinon pas acces a /admin/
        queryset.update(is_staff=True)
        self.message_user(request, f'{queryset.count()} ajouté(s) à la liste')

    @admin.action(description='Retirer de la liste')
    def remove_from_liste(self, request, queryset):
        group = Group.objects.get(name=LISTE_GROUP)
        for user in queryset:
            user.groups.remove(group)
        # on touche pas aux superusers, sinon on se lock dehors
        queryset.filter(is_superuser=False).update(is_staff=False)
        if queryset.filter(is_superuser=True).exists():
            self.message_user(request, 'Superusers gardent leur acces admin', messages.WARNING)
        self.message_user(request, f'{queryset.count()} retiré(s) de la liste')
