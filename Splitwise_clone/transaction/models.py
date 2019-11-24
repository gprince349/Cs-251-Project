from django.db import models

# Create your models here.

class id_trans(models.Model):
    myid = models.IntegerField()
    fid = models.IntegerField() # primary key  
    desc = models.TextField()
    owe = models.IntegerField()
    lent = models.IntegerField()
    pbu = models.IntegerField()
    pbf = models.IntegerField()
    obu = models.IntegerField()
    obf = models.IntegerField()


class grp_trans(models.Model):
    tid = models.IntegerField()
    gid=models.IntegerField()
    pid=models.IntegerField()
    paid=models.IntegerField()
    owe=models.IntegerField()

# class grp_net_bal(models.Model):
#     gid=models.IntegerField()
#     pid=models.IntegerField()
#     net=models.IntegerField()

class grp_trans_desc(models.Model):
    gid=models.IntegerField()
    desc=models.TextField(default="")