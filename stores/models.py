from django.db import models

class Cart(models.Model):
    quantity    = models.PositiveIntegerField(default = 0)
    user        = models.ForeignKey('user.User', on_delete = models.SET_NULL, null = True)
    gift_set    = models.ForeignKey('product.GiftSet', on_delete = models.SET_NULL, null = True)
    razor_set   = models.ForeignKey('product.RazorSet', on_delete = models.SET_NULL, null = True)
    blades      = models.ForeignKey('product.Blade', on_delete = models.SET_NULL, null = True)
    shaving_gel = models.ForeignKey('product.ShavingGel', on_delete = models.SET_NULL, null = True)
    after_shave = models.ForeignKey('product.AfterShave', on_delete = models.SET_NULL, null = True)
    color       = models.ForeignKey('product.Color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'carts'
