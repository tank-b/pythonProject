from django.db import models
from datetime import datetime







class Polls(models.Model):
    poll_id = models.AutoField(primary_key=True, auto_created=True, default = "1")
    advancement = models.DecimalField(max_digits=3, decimal_places=0, null=False)
    difficulty = models.CharField(max_length=15, null=False)
    progression = models.CharField(max_length=15, null=False)

class Sessions(models.Model):
    session_id = models.AutoField(primary_key=True, auto_created=True)
    opening_time = models.DateTimeField(default=datetime.now)
    closing_time = models.DateTimeField(default=datetime.now)

class Students(models.Model):
    student_id = models.AutoField(primary_key=True, auto_created=True, default = "1")
    login = models.CharField(max_length=15,unique=True, null=False)
    first_name= models.CharField(max_length=120, null=False)
    last_name = models.CharField(max_length=120, null=False)
    email = models.CharField(max_length=120,unique=True,)
    password = models.CharField(max_length=120, null=False)
    hashed = models.CharField(max_length=120, null=False)
    salt = models.CharField(max_length=120, null=False)
    first_login = models.DateTimeField(default=datetime.now, null=False)