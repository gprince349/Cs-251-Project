from django.db import models

# Create your models here.

# class user_image(models.Model):
#     myid = models.IntegerField()
#     image = models.ImageField(upload_to='profile_image', blank=True)

class group_name(models.Model):
    name = models.TextField()


class group_member(models.Model):
    gid = models.IntegerField()
    pid = models.IntegerField()
    net = models.IntegerField(default=0)




class Destination(models.Model):
    name = models.TextField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='pics')
    desc = models.TextField()
    offer = models.BooleanField(default=False)

# class global_variables(models.Model):

#     name  = models.TextField()
#     id = models.TextField()

# class transaction_variables(models.Model):

#     id = models.TextField()
#     trans_id = models.TextField()

class GROUP_MEMBERSHIP(models.Model):
    pid = models.TextField()
    gid = models.TextField()
    group_name = models.TextField(max_length=100)
    joined_date = models.TextField()
    left_date = models.TextField()

class id_friends(models.Model):
    myid = models.IntegerField()
    fid = models.IntegerField() # primary key
    owe = models.IntegerField()
    lent = models.IntegerField()


# class id_cummulative(models.Model):

#     fid = models.TextField # primary key
#     owe = models.IntegerField()
#     lent = models.IntegerField()

# class grp_member(models.Model):

#     pid = models.TextField # primary key
#     owe = models.IntegerField()
#     lent = models.IntegerField()

# class grp_trans(models.Model):

#     tid = models.TextField()
#     pid = models.TextField()
#     desc = models.TextField(max_length=100)
#     owe = models.IntegerField()
#     lent = models.IntegerField()

# class grp_pairwise(models.Model):

#     p1_id = models.TextField() # combined primary key
#     p2_id = models.TextField() # combined primary key
#     p1_lent = models.IntegerField()
#     p2_lent = models.IntegerField()
