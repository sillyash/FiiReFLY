"""Role "Liste" : les membres de la liste peuvent gerer le contenu depuis l'admin."""

LISTE_GROUP = 'Liste'

# (app, modele) -> actions autorisées
_PERMS = {
    'soiree': ['add', 'change', 'delete', 'view'],
    'membre': ['add', 'change', 'delete', 'view'],
    'pole': ['add', 'change', 'delete', 'view'],
    # change = pouvoir masquer (is_visible), pas de add : on poste via le site
    'livredorentry': ['change', 'delete', 'view'],
}

LISTE_PERMISSIONS = sorted(
    f'core.{action}_{model}' for model, actions in _PERMS.items() for action in actions
)


def sync_liste_group(**kwargs):
    """Cree le groupe + remet ses perms a jour, lancé apres chaque migrate."""
    from django.contrib.auth.models import Group, Permission

    group, _ = Group.objects.get_or_create(name=LISTE_GROUP)
    codenames = [p.split('.', 1)[1] for p in LISTE_PERMISSIONS]
    perms = Permission.objects.filter(content_type__app_label='core', codename__in=codenames)
    group.permissions.set(perms)
