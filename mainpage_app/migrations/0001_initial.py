# Generated by Django 5.1 on 2024-08-16 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumptionIndustry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry', models.CharField(max_length=30)),
                ('consumption', models.FloatField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ConsumptionRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumption', models.FloatField()),
                ('city', models.CharField(max_length=30)),
                ('date2', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='KeywordVolume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100)),
                ('count', models.IntegerField()),
                ('city', models.CharField(max_length=30)),
                ('date2', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='VisitingPopulation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('foreigner', models.IntegerField()),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VisitorJeju',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VisitorRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('state', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wind_speed', models.FloatField()),
                ('relative_humidity', models.FloatField()),
                ('rain_fall', models.FloatField()),
                ('temperature', models.FloatField()),
                ('date', models.DateField()),
            ],
        ),
    ]
