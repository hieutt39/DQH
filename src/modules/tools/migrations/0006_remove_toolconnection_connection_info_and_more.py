# Generated by Django 4.2.4 on 2023-08-19 03:14

from django.db import migrations, models
import src.modules.tools.models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0005_toolexecute_destination_toolexecute_source_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolconnection',
            name='connection_info',
        ),
        migrations.AddField(
            model_name='toolconnection',
            name='db_database',
            field=models.CharField(default='web_reservation', max_length=255, verbose_name='Database'),
        ),
        migrations.AddField(
            model_name='toolconnection',
            name='db_driver',
            field=models.CharField(default='mysql', max_length=255, verbose_name='Driver'),
        ),
        migrations.AddField(
            model_name='toolconnection',
            name='db_host',
            field=models.CharField(default='127.0.0.1', max_length=255, verbose_name='Host'),
        ),
        migrations.AddField(
            model_name='toolconnection',
            name='db_password',
            field=models.CharField(default='root', max_length=255, verbose_name='Password'),
        ),
        migrations.AddField(
            model_name='toolconnection',
            name='db_port',
            field=models.CharField(default='3306', max_length=255, verbose_name='Port'),
        ),
        migrations.AddField(
            model_name='toolconnection',
            name='db_user',
            field=models.CharField(default='root', max_length=255, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='toolconnection',
            name='extra',
            field=models.JSONField(default=dict, encoder=src.modules.tools.models.PrettyJSONEncoder, null=True, verbose_name='Extra'),
        ),
        migrations.AlterField(
            model_name='toolconnection',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Display Name'),
        ),
    ]
