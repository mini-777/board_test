# Generated by Django 3.1.3 on 2020-11-24 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_boardmember_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardmember',
            name='carNum',
            field=models.CharField(default='11123', max_length=100, verbose_name='차량번호'),
            preserve_default=False,
        ),
    ]