# Generated by Django 4.0.4 on 2022-07-07 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeyUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_file', models.FileField(upload_to='')),
                ('key_passphrase', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SftpConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(default='198.19.243.251', max_length=20)),
                ('port', models.IntegerField(default=2222)),
                ('username', models.CharField(default='tester', max_length=20)),
                ('password', models.CharField(default='', max_length=20)),
            ],
        ),
    ]