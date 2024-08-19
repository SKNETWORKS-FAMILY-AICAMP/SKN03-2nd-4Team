from django.contrib import admin
from .models import (
    KeywordVolume,
    VisitingPopulation,
    VisitorJeju,
    VisitorRegion,
    ConsumptionRegion,
    ConsumptionIndustry,
    Weather,
)

admin.site.register(KeywordVolume)
admin.site.register(VisitingPopulation)
admin.site.register(VisitorJeju)
admin.site.register(VisitorRegion)
admin.site.register(ConsumptionRegion)
admin.site.register(ConsumptionIndustry)
admin.site.register(Weather)
