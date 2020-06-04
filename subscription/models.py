from django.db import models

class Question(models.Model):
    question = models.CharField(max_length = 500)

    class Meta:
        db_table = 'questions'

class Answer(models.Model):
    answer      = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500, null = True)
    question    = models.ForeignKey('Question', on_delete = models.SET_NULL, null = True)
    color       = models.ForeignKey('stores.color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'answers'

class SubscriptionPeriod(models.Model):
    name        = models.CharField(max_length = 20)
    description = models.CharField(max_length = 500)
    period      = models.IntegerField(default = 1)
    period_type = models.ForeignKey(PeriodType)

    class Meta:
        db_table = 'durations'

class PeriodType:
    name = models.CharField(max_length = 20)
