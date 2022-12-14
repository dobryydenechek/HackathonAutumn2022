# Generated by Django 4.1.2 on 2022-10-21 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=255, null=True)),
                ('lastname', models.CharField(blank=True, max_length=255, null=True)),
                ('telephone', models.CharField(blank=True, max_length=20, null=True)),
                ('old', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('male', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Man'), (2, 'Woman')], null=True)),
                ('adres', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
    ]
