# Generated by Django 4.2.6 on 2023-12-13 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_article_article_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomment',
            name='created_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='articlecomment',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
