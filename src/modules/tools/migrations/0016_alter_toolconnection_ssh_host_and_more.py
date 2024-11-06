# Generated by Django 4.2.4 on 2023-11-13 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0015_toolapicollectionresultdetail_compare_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolconnection',
            name='ssh_host',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='SSH Host'),
        ),
        migrations.AlterField(
            model_name='toolconnection',
            name='ssh_password',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='SSH Password'),
        ),
        migrations.AlterField(
            model_name='toolconnection',
            name='ssh_port',
            field=models.CharField(default='22', max_length=255, null=True, verbose_name='SSH Port'),
        ),
        migrations.AlterField(
            model_name='toolconnection',
            name='ssh_rsa',
            field=models.FileField(default='', help_text='Enter RSA file', null=True, upload_to='assets/rsa', verbose_name='RSA file'),
        ),
        migrations.AlterField(
            model_name='toolconnection',
            name='ssh_user',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='SSH Username'),
        ),
    ]