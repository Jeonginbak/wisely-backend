from django.db import models

class User(models.Model):
    email         = models.EmailField(max_length = 200, unique = True)
    password      = models.CharField(max_length = 500)
    phone         = models.CharField(max_length = 45, unique = True)
    birth         = models.DateField()
    name          = models.CharField(max_length = 45, unique = True)
    gender        = models.ForeignKey('Gender', on_delete = models.SET_NULL, null = True)
    alarm_confirm = models.BooleanField()
    created_at    = models.DateTimeField(auto_now_add = True)
    updated_at    = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'

class Gender(models.Model):
    name = models.CharField(max_length = 10)

    class Meta:
        db_table = 'genders'

