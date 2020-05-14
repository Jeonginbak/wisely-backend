from django.db import models

class GiftSet(models.Model):
    name  = models.CharField(max_length = 20)
    price = models.PositiveIntegerField(default = 0)
    image = models.ForeignKey('GiftSetImage', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'gift_sets'

class GiftSetImage(models.Model):
    product_image = models.URLField(max_length = 2000)
    color         = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'gift_set_images'

class RazorSet(models.Model):
    name  = models.CharField(max_length = 20)
    price = models.PositiveIntegerField(default = 0)
    image = models.ForeignKey('RazorSetImage', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'razor_sets'

class RazorSetImage(models.Model):
    product_image = models.URLField(max_length = 2000)
    result_image  = models.URLField(max_length = 2000)
    color         = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'razor_set_images'

class Blade(models.Model):
    name         = models.CharField(max_length = 20)
    price        = models.PositiveIntegerField(default = 0)
    image        = models.URLField(max_length = 2000)
    result_image = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'blades'

class ShavingGel(models.Model):
    name         = models.CharField(max_length = 20)
    price        = models.PositiveIntegerField(default = 0)
    image        = models.URLField(max_length = 2000)
    result_image = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'shaving_gels'

class AfterShave(models.Model):
    name                  = models.CharField(max_length = 20)
    price                 = models.PositiveIntegerField(default = 0)
    after_shave_skin_type = models.ManyToManyField('SkinType', through = 'AfterShaveSkinType')

    class Meta:
        db_table = 'after_shaves'

class AfterShaveSkinType(models.Model):
    after_shave  = models.ForeignKey('AfterShave', on_delete = models.SET_NULL, null = True)
    skin_type    = models.ForeignKey('SkinType', on_delete = models.SET_NULL, null = True)
    image        = models.URLField(max_length = 2000)
    result_image = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'after_shaves_skin_types'

class SkinType(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = 'skin_types'

class Color(models.Model):
    name = models.CharField(max_length = 20)
    code = models.CharField(max_length = 10)

    class Meta:
        db_table = 'colors'

class RazorImages(models.Model):
    image_type       = models.CharField(max_length = 20)
    image            = models.URLField(max_length = 2000)
    background_image = models.URLField(max_length = 2000)
    color            = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'razor_images'
