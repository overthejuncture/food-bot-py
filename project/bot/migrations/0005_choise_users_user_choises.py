# Generated by Django 4.0.5 on 2022-06-15 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_user_rename_choise_id_choiseuser_choise_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='choise',
            name='users',
            field=models.ManyToManyField(through='bot.ChoiseUser', to='bot.user'),
        ),
        migrations.AddField(
            model_name='user',
            name='choises',
            field=models.ManyToManyField(through='bot.ChoiseUser', to='bot.choise'),
        ),
    ]