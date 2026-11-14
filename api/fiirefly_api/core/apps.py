from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fiirefly_api.core'

    def ready(self):
        from .roles import sync_liste_group

        # les perms sont créées en post_migrate aussi, donc on passe apres
        post_migrate.connect(sync_liste_group, sender=self)
