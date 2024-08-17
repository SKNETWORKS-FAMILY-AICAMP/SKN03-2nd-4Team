# data_management/models.py

from django.db import models


class KeywordVolume(models.Model):
    keyword = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    date = models.DateField()  # 필드 이름이 'date'인지 확인하세요
    count = models.IntegerField()


class VisitingPopulation(models.Model):
    city = models.CharField(max_length=30)
    date = models.DateField()
    foreigner = models.IntegerField()
    count = models.IntegerField()


class VisitorJeju(models.Model):
    date = models.DateField()
    count = models.IntegerField()


class VisitorRegion(models.Model):
    date = models.DateField()
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    count = models.IntegerField()


class ConsumptionRegion(models.Model):
    consumption = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=30)
    date2 = models.DateField()


class Weather(models.Model):
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    relative_humidity = models.DecimalField(max_digits=5, decimal_places=2)
    rain_fall = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()


class ConsumptionIndustry(models.Model):
    industry = models.CharField(max_length=30)
    consumption = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
