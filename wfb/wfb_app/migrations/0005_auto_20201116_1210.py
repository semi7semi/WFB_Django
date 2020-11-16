# Generated by Django 3.0.6 on 2020-11-16 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wfb_app', '0004_gameresults_objectives_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_armys',
        ),
        migrations.CreateModel(
            name='UserArmies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('army', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wfb_app.Armys')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wfb_app.User')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_armies',
            field=models.ManyToManyField(through='wfb_app.UserArmies', to='wfb_app.Armys'),
        ),
    ]