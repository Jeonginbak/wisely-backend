import json

from django.http         import JsonResponse,HttpResponse
from django.views        import View

from .models             import Cart
from product.models      import RazorSet, Color

class RazorCartView(View):
    def post(self, request):
        data = json.loads(request.body)
        try :
            razor = RazorSet.objects.select_related('image', 'image__color').get(image__color = data['color_id'])

            if Cart.objects.filter(color_id = data['color_id']).exists():
                cart = Cart.objects.get(color_id = data['color_id'])
                cart.quantity += 1
                cart.save()

                return HttpResponse(status = 200)

            Cart.objects.create(
                razor_set = razor,
                quantity = 1,
                color = Color.objects.get(id = data['color_id'])
            )

            return HttpResponse(status = 200)

        except RazorSet.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status = 400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
