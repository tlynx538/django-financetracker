# Generated by Django 3.0.8 on 2021-01-04 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expenseinfo',
            old_name='user',
            new_name='user_expense',
        ),
    ]
