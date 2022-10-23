# Generated by Django 4.1.2 on 2022-10-23 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0007_alter_trafic_chksum_alter_trafic_dataofs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafic',
            name='ask',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='chksum',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='dataofs',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='dport',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='seq',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='sport',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='timestamp',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trafic',
            name='window',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]