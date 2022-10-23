# Generated by Django 4.1.2 on 2022-10-23 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_alter_csvfile_file_alter_pcapfile_file_package'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trafic',
            name='end',
        ),
        migrations.RemoveField(
            model_name='trafic',
            name='start',
        ),
        migrations.AddField(
            model_name='trafic',
            name='ask',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trafic',
            name='chksum',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trafic',
            name='dataofs',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trafic',
            name='dport',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trafic',
            name='seq',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trafic',
            name='sport',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trafic',
            name='timestamp',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='trafic',
            name='window',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'chats'), (1, 'video'), (2, 'files'), (3, 'email'), (4, 'sftp'), (5, 'ftps')], null=True),
        ),
    ]