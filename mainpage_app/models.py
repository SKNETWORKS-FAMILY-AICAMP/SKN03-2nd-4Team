from django.db import models


from django.db import models


class KeywordVolume(models.Model):
    keyword = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    date = models.DateField()  # date 필드가 정의되어 있어야 합니다.
    count = models.IntegerField()

    def __str__(self):
        return f"{self.keyword} - {self.city} - {self.date}"


class VisitingPopulation(models.Model):
    city = models.CharField(max_length=100)
    foreigner = models.CharField(max_length=10)  # 숫자가 아닌 문자열로 변경
    date = models.DateField()
    count = models.IntegerField()


class VisitorJeju(models.Model):
    date = models.DateField()
    personal_trip = models.IntegerField(default=0)
    partial_package = models.IntegerField(default=0)
    package = models.IntegerField(default=0)
    leisure = models.IntegerField(default=0)
    work = models.IntegerField(default=0)
    recreation = models.IntegerField(default=0)
    visit_rel = models.IntegerField(default=0)
    edu = models.IntegerField(default=0)
    etc = models.IntegerField(default=0)
    jpn = models.IntegerField(default=0)
    chn = models.IntegerField(default=0)
    hkg = models.IntegerField(default=0)
    twn = models.IntegerField(default=0)
    sgp = models.IntegerField(default=0)
    mys = models.IntegerField(default=0)
    idn = models.IntegerField(default=0)
    vnm = models.IntegerField(default=0)
    tha = models.IntegerField(default=0)
    asia_etc = models.IntegerField(default=0)
    usa = models.IntegerField(default=0)
    west_etc = models.IntegerField(default=0)


class VisitorRegion(models.Model):
    date = models.DateField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    count = models.IntegerField()


class ConsumptionRegion(models.Model):
    consumption = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    date = models.DateField()


class ConsumptionIndustry(models.Model):
    industry = models.CharField(max_length=100)
    consumption = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()


class Weather(models.Model):
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    relative_humidity = models.DecimalField(max_digits=5, decimal_places=2)
    rain_fall = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
