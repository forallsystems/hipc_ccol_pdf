from django.db import models
    
class School(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=256)
    
class Flyer(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=256)
    subscribed = models.BooleanField(default=True)
    title = models.CharField(max_length=256)
    school = models.ForeignKey(School)
    grade = models.IntegerField()
    subject = models.CharField(max_length=256)
    