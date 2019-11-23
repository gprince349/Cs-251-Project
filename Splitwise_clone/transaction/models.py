from django.db import models

# Create your models here.
class id_trans(models.Model):
    myid = models.IntegerField()
    fid = models.IntegerField() # primary key  
    desc = models.TextField()
    owe = models.IntegerField()
    lent = models.IntegerField()