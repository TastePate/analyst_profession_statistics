from django.db import models


class Vacancy(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    key_skills = models.TextField(blank=True, null=True)
    salary_from = models.FloatField(blank=True, null=True)
    salary_to = models.FloatField(blank=True, null=True)
    salary_currency = models.CharField(max_length=4, blank=True, null=True)
    area_name = models.CharField(max_length=50, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)



