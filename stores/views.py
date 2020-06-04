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

class CartView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)

        try:
            with transaction.atomic():
                sid   = transaction.savepoint()
                order = Order.objects.filter(
                    user = request.user,
                    order_status_id = PENDING_ORDER
                ).exists()

                if not order:
                    Order.objects.create(
                        order_num       = 'wisely_' + uuid.uuid4().hex,
                        user            = request.user,
                        order_status_id = 1
                    )

                user_order = Order.objects.get(
                    user            = request.user,
                    order_status_id = PENDING_ORDER
                )

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
                order          = user_order
            )

            if Order.objects.filter(user = request.user).exists():
                orders = (
                    Order
                    .objects
                    .select_related('user','order_status')
                    .prefetch_related('cart_set')
                    .filter(
                        user            = request.user,
                        order_status_id = ORDER_STATUS_PENDING
                    )

                carts = [
                    {
                        'id'           : order.id,
                        'order_number' : order.order_num,
                        'name'         : order.user.name,
                        'address'      : order.address,
                        'phone_number' : order.phone_number,
                        'memo'         : order.memo,
                        'order_status' : order.order_status.status,
                        'created_at'   : order.created_at,
                        'cart'         : {'name': product.name, 'id': product.id for product in products}

                        'cart'         : [{
                                'gift_id'           : cart['gift_set__id'],
                                'gift_set'          : cart['gift_set__name'],
                                'gift_color'        : cart['gift_set__image__color__name'],
                                'gift_price'        : cart['gift_set__price'],
                                'gift_image'        : cart['gift_set__image__product_image'],
                                'razor_id'          : cart['razor_set__id'],
                                'razor_set'         : cart['razor_set__name'],
                                'razor_color'       : cart['razor_set__image__color__name'],
                                'razor_price'       : cart['razor_set__price'],
                                'razor_image'       : cart['razor_set__image__product_image'],
                                'blade_id'          : cart['blade__id'],
                                'blade'             : cart['blade__name'],
                                'blade_price'       : cart['blade__price'],
                                'blade_image'       : cart['blade__image'],
                                'shaving_gel_id'    : cart['shaving_gel__id'],
                                'shaving_gel'       : cart['shaving_gel__name'],
                                'shaving_gel_price' : cart['shaving_gel__price'],
                                'shaving_gel_image' : cart['shaving_gel__image'],
                                'after_shave_id'    : cart['after_shave__id'],
                                'after_shave'       : cart['after_shave__after_shave__name'],
                                'skin_type'         : cart['after_shave__skin_type__name'],
                                'after_shave_price' : cart['after_shave__after_shave__price'],
                                'after_shave_image' : cart['after_shave__image']
                                }for cart in (order.cart_set.select_related(
                                'gift_set',
                                'gift_set__image',
                                'gift_set__image__color',
                                'razor_set',
                                'razor_set__image',
                                'razor_set__image__color',
                                'blade',
                                'shaving_gel',
                                'after_shave',
                                'after_shave__after__shave',
                                'after_shave__skin_type',
                                ).filter(order_id = order.id).values(
                                    'gift_set__id',
                                    'gift_set__name',
                                    'gift_set__image__color__name',
                                    'gift_set__price',
                                    'gift_set__image__product_image',
                                    'razor_set__id',
                                    'razor_set__name',
                                    'razor_set__image__color__name',
                                    'razor_set__price',
                                    'razor_set__image__product_image',
                                    'blade__id',
                                    'blade__name',
                                    'blade__price',
                                    'blade__image',
                                    'shaving_gel__id',
                                    'shaving_gel__name',
                                    'shaving_gel__price',
                                    'shaving_gel__image',
                                    'after_shave__id',
                                    'after_shave__after_shave__name',
                                    'after_shave__skin_type__name',
                                    'after_shave__after_shave__price',
                                    'after_shave__image'
                                    ).order_by('gift_set__id','razor_set__id', 'blade__id', 'shaving_gel__id', 'after_shave__id').distinct()
                                )
                            ]
                } for order in orders]

                return JsonResponse({'data' : carts}, status = 200)

        except IntegrityError:
            return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status = 400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
