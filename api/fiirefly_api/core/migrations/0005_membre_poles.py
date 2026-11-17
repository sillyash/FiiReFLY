from django.db import migrations, models


def fk_to_m2m(apps, schema_editor):
    Membre = apps.get_model('core', 'Membre')
    for membre in Membre.objects.exclude(pole=None):
        membre.poles.add(membre.pole_id)


def m2m_to_fk(apps, schema_editor):
    # retour arriere : on garde que le pole principal
    Membre = apps.get_model('core', 'Membre')
    for membre in Membre.objects.all():
        membre.pole = membre.poles.order_by('ordre', 'nom').first()
        membre.save(update_fields=['pole'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_pole_couleur_help'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membre',
            options={'ordering': ['ordre', 'nom']},
        ),
        migrations.AddField(
            model_name='membre',
            name='poles',
            field=models.ManyToManyField(blank=True, related_name='+', to='core.pole'),
        ),
        migrations.RunPython(fk_to_m2m, m2m_to_fk),
        migrations.RemoveField(
            model_name='membre',
            name='pole',
        ),
        migrations.AlterField(
            model_name='membre',
            name='poles',
            field=models.ManyToManyField(blank=True, related_name='membres', to='core.pole'),
        ),
    ]
