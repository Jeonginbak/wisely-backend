import json

from django.http    import JsonResponse, HttpResponse
from django.views   import View
from django.db      import IntegrityError

from user.models    import User
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
Cart
)

class CartAddView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if sum(value == None for value in data.values()) < 4:
                return JsonResponse({'message' : 'BAD_REQUEST'}, status = 400)

            if Cart.objects.filter(
                gift_set_id    = data['gift_set_id'], 
                razor_set_id   = data['razor_set_id'], 
                blade_id       = data['blade_id'], 
                shaving_gel_id = data['shaving_gel_id'], 
                after_shave_id = data['after_shave_id']).exists():

                cart = Cart.objects.filter(
                    gift_set_id    = data['gift_set_id'], 
                    razor_set_id   = data['razor_set_id'], 
                    blade_id       = data['blade_id'], 
                    shaving_gel_id = data['shaving_get_id'], 
                    after_shave_id = data['after_shave_id'])

                cart.quantity += 1
                cart.save()
                return HttpResponse(status = 200)

            Cart.objects.create(
                gift_set_id    = data['gift_set_id'],
                razor_set_id   = data['razor_set_id'],
                blade_id       = data['blade_id'],
                shaving_gel_id = data['shaving_gel_id'],
                after_shave_id = data['after_shave_id'],
                quantity       = 1
                )
            return HttpResponse(status = 200)

        except IntegrityError:
            return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXISTS'}, status = 400)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)