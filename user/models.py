from django.db import models

class User(models.Model):
    email         = models.EmailField(max_length = 200, unique = True)
    password      = models.CharField(max_length = 500)
    phone         = models.CharField(max_length = 50, unique = True)
    birth         = models.DateField(null=True)
    name          = models.CharField(max_length = 50)
    gender        = models.CharField(max_length = 10)
    alarm_confirm = models.BooleanField(null=True)
    created_at    = models.DateTimeField(auto_now_add = True)
    updated_at    = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'
