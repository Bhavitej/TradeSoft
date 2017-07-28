from django.contrib.auth.models import Permission, User
from django.db import models


class Company(models.Model):
    '''user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)'''
    user = models.ForeignKey(User, default=1)
    company_name=models.CharField(max_length=250)
    company_stock_code=models.CharField(max_length=20)
    company_logo=models.FileField(null=True)
    is_favorite = models.BooleanField(default=False)
    is_selected=models.BooleanField(default=False)

    demand_daily_under_proc= models.BooleanField(default=False)
    demand_weekly_under_proc= models.BooleanField(default=False)
    demand_monthly_under_proc= models.BooleanField(default=False)
    demand_daily_entry=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    demand_daily_stoploss=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    demand_weekly_entry=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    demand_weekly_stoploss=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    demand_monthly_entry=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    demand_monthly_stoploss=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    demand_daily_lastmodified_date=models.CharField(max_length=100,default="Not Yet Run")
    demand_weekly_lastmodified_date=models.CharField(max_length=100,default="Not Yet Run")
    demand_monthly_lastmodified_date=models.CharField(max_length=100,default="Not Yet Run")

    supply_daily_under_proc= models.BooleanField(default=False)
    supply_weekly_under_proc= models.BooleanField(default=False)
    supply_monthly_under_proc= models.BooleanField(default=False)
    supply_daily_entry=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    supply_daily_stoploss=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    supply_weekly_entry=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    supply_weekly_stoploss=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    supply_monthly_entry=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    supply_monthly_stoploss=models.DecimalField(max_digits=100, decimal_places=4,null=True)
    supply_daily_lastmodified_date=models.CharField(max_length=100,default="Not Yet Run")
    supply_weekly_lastmodified_date=models.CharField(max_length=100,default="Not Yet Run")
    supply_monthly_lastmodified_date=models.CharField(max_length=100,default="Not Yet Run")

    def __str__(self):
        return self.company_name + ' - ' + self.company_stock_code


'''class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title'''
