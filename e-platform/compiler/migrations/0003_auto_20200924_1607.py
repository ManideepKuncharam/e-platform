# Generated by Django 2.1.1 on 2020-09-24 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0002_auto_20200924_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cquestions',
            name='constraints',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='ctestcases',
            name='testinput',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='ctestcases',
            name='testoutput',
            field=models.TextField(max_length=500),
        ),
    ]