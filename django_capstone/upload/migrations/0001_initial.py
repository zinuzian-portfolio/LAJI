# Generated by Django 2.1.7 on 2019-04-07 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoUploadModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='new video', max_length=200)),
                ('videoFile', models.FileField(upload_to='videos/')),
            ],
        ),
    ]