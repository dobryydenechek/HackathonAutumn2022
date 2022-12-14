# Generated by Django 4.1.2 on 2022-10-23 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0006_remove_trafic_persone_trafic_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafic',
            name='chksum',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='dataofs',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='dport',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='sport',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='type',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'chats'), (1, 'video'), (2, 'files'), (3, 'email'), (4, 'sftp'), (5, 'ftps')], null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='window',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
