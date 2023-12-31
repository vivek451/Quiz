# Generated by Django 4.2.7 on 2023-11-29 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('response', models.IntegerField(choices=[(0, 'Never'), (1, 'Sometimes'), (2, 'Often')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
