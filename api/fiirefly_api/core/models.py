from django.db import models


class Soiree(models.Model):
    titre = models.CharField(max_length=100)
    date = models.DateTimeField(help_text='Date et heure de début')
    lieu = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200, blank=True)
    lien = models.URLField(blank=True, help_text='Billetterie ou infos')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'soirée'

    def __str__(self):
        return f'{self.titre} ({self.date:%d/%m/%Y})'


class LivreDorEntry(models.Model):
    nom = models.CharField(max_length=50)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    # Anonymous submissions stay hidden until approved in the admin.
    is_visible = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "message du livre d'or"
        verbose_name_plural = "messages du livre d'or"

    def __str__(self):
        return f'{self.nom} : {self.message[:40]}'
