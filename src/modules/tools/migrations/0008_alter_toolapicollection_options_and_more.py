# Generated by Django 4.2.4 on 2023-08-24 13:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import src.modules.tools.models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0007_toolapicollection_alter_toolexecute_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='toolapicollection',
            options={'ordering': ['-created_at', 'name'], 'verbose_name': 'Api Collections', 'verbose_name_plural': 'Api Collections'},
        ),
        migrations.AlterModelOptions(
            name='toolconnection',
            options={'ordering': ['-updated_at', '-created_at'], 'verbose_name': 'DB Connections', 'verbose_name_plural': 'DB Connections'},
        ),
        migrations.AlterField(
            model_name='toolapicollection',
            name='collection',
            field=models.FileField(help_text='Enter a collection file to Execute', upload_to='assets/collections', verbose_name='Collection file'),
        ),
        migrations.CreateModel(
            name='ToolApiCollectionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict, encoder=src.modules.tools.models.PrettyJSONEncoder, null=True, verbose_name='Data')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('tool_execute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tools.toolconnection', verbose_name='tool collection result')),
            ],
            options={
                'verbose_name': 'Api Collection results',
                'verbose_name_plural': 'Api Collection results',
                'db_table': 'tool_api_collection_result',
                'ordering': ['-created_at'],
            },
            managers=[
                ('objects', src.modules.tools.models.LogEntryManager()),
            ],
        ),
    ]
