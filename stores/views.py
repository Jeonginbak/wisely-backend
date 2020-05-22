import json, uuid

from django.http    import JsonResponse, HttpResponse
from django.views   import View
from django.db      import IntegrityError, transaction
from django.db.models import Count

from user.models    import User
from user.utils     import login_required
from .models        import (
GiftSet,
GiftSetImage,
RazorSet,
RazorSetImage,
Blade,
ShavingGel,
AfterShave,
AfterShaveSkinType,
SkinType,
Color,
Cart,
Order
)

ORDER_STATUS_PENDING = 1

class CartView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)
        try:
            with transaction.atomic():
                sid = transaction.savepoint()

                if not Order.objects.filter(user = request.user, order_status_id = 1).exists():
                    Order.objects.create(
                        order_num       = 'wisely_' + uuid.uuid4().hex,
                        user            = request.user,
                        order_status_id = 1
                    )

                user_order = Order.objects.get(user = request.user, order_status_id = ORDER_STATUS_PENDING)

                if sum(value == None for value in data.values()) < 4:
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'message' : 'BAD_REQUEST'}, status = 400)

            Cart.objects.create(
                user           = request.user,
                gift_set_id    = data['gift_set_id'],
                razor_set_id   = data['razor_set_id'],
                blade_id       = data['blade_id'],
                shaving_gel_id = data['shaving_gel_id'],
                after_shave_id = data['after_shave_id'],
                quantity       = 1,
                order          = user_order
                )
            return HttpResponse(status = 200)

        except IntegrityError:
            return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXISTS'}, status = 400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_required
    def get(self, request):
        order = Order.objects.get(user = request.user, order_status_id = ORDER_STATUS_PENDING)
        carts = order.cart_set.all()

        gift_set    = carts.select_related(
                      'gift_set', 'gift_set__image', 'gift_set__image__color').filter(
                       gift_set_id__isnull = False)
        razor_set   = carts.select_related(
                      'razor_set', 'razor_set__image', 'razor_set__image__color').filter(
                       razor_set_id__isnull = False)
        blades      = carts.select_related('blade').filter(
                      blade_id__isnull = False)
        shaving_gel = carts.select_related('shaving_gel').filter(
                      shaving_gel_id__isnull = False)
        after_shave = carts.select_related(
                      'after_shave','after_shave__after_shave', 'after_shave__skin_type').filter(
                       after_shave_id__isnull = False)

        gift_set =[{
            'name'     : giftset.gift_set.name,
            'color'    : giftset.gift_set.image.color.name,
            'price'    : giftset.gift_set.price,
            'quantity' : giftset.quantity,
            'image'    : giftset.gift_set.image.product_image
        } for giftset in gift_set]

        razor_set = [{
            'name'     : razorset.razor_set.name,
            'color'    : razorset.razor_set.image.color.name,
            'price'    : razorset.razor_set.price,
            'quantity' : razorset.quantity,
            'image'    : razorset.razor_set.image.product_image
        } for razorset in razor_set]

        blades = [{
            'name'     : blade.blade.name,
            'price'    : blade.blade.price,
            'quantity' : blade.quantity,
            'image'    : blade.blade.image
        } for blade in blades]

        shaving_gel = [{
            'name'     : shavinggel.shaving_gel.name,
            'price'    : shavinggel.shaving_gel.price,
            'quantity' : shavinggel.quantity,
            'image'    : shavinggel.shaving_gel.image,
         } for shavinggel in shaving_gel]

        after_shave = [{
            'name'      : aftershave.after_shave.after_shave.name,
            'skin_type' : aftershave.after_shave.skin_type.name,
            'price'     : aftershave.after_shave.after_shave.price,
            'quantity'  : aftershave.quantity,
            'image'     : aftershave.after_shave.image
        } for aftershave in after_shave]

        return JsonResponse({
            'gift_set'    : gift_set,
            'razor_set'   : razor_set,
            'blades'      : blades,
            'shaving_gel' : shaving_gel,
            'after_shave' : after_shave
            }, status = 200)
