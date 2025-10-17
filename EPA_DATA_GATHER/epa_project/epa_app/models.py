from django.db import models
# Create your models here.

class siteData(models.Model):
  site_id = models.CharField(max_length=15)
  state = models.CharField(max_length=50, default="unknown")
  county = models.CharField(max_length=100, default="unknown")
  pollutant = models.CharField(max_length=70)
  value = models.FloatField()
  units = models.CharField(max_length=100, default="unknown")
  date = models.DateField()
  
  def __str__(self):
    return f"{self.county}, {self.state}: {self.site_id} - {self.pollutant}"
