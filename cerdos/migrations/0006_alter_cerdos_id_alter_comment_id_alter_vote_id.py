# Generated by Django 4.2.13 on 2025-06-19 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cerdos', '0005_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cerdos',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
