# Generated by Django 5.1.4 on 2024-12-25 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0006_rename_post_saveitem_post_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('Женский', 'Женский'), ('Мужской', 'Мужской'), ('Пропустить', 'Пропустить'), ('Не указывать', 'Не указывать')], default='Другой', max_length=99),
        ),
    ]
