from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from .images import square_webp


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
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='livre_dor_entries',
    )
    # Name at posting time, kept even if the user is deleted.
    nom = models.CharField(max_length=50)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Can be hidden from the admin.
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        # un seul message par personne, les auteurs NULL (user supprimé, admin) comptent pas
        constraints = [
            models.UniqueConstraint(fields=['auteur'], name='livre_dor_un_par_auteur'),
        ]
        verbose_name = "message du livre d'or"
        verbose_name_plural = "messages du livre d'or"

    def __str__(self):
        return f'{self.nom} : {self.message[:40]}'


class Pole(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    couleur = models.CharField(
        max_length=7,
        default='#cb6c89',
        validators=[RegexValidator(r'^#[0-9a-fA-F]{6}$', 'Format #RRGGBB stp')],
        help_text='Couleur des lucioles (hex, ex #cb6c89)',
    )
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = 'pôle'

    def __str__(self):
        return self.nom


class Membre(models.Model):
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True, help_text='Prez, trez, respo com...')
    poles = models.ManyToManyField(Pole, blank=True, related_name='membres')
    photo = models.ImageField(
        upload_to='trombi/', blank=True, help_text='Crop en carré + compressée auto'
    )
    description = models.TextField(blank=True)
    ordre = models.PositiveSmallIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        # le tri par pole se fait dans la vue (M2M = doublons si on trie dessus ici)
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        old = None
        if self.pk:
            old = Membre.objects.filter(pk=self.pk).values_list('photo', flat=True).first()
        # nouvelle photo uploadée -> on la traite, et on vire l'ancienne
        if self.photo and not self.photo._committed:
            processed = square_webp(self.photo)
            self.photo.save(processed.name, processed, save=False)
        super().save(*args, **kwargs)
        if old and old != self.photo.name:
            self.photo.storage.delete(old)
