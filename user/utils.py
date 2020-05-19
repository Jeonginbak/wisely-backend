import jwt

from django.http     import JsonResponse

from wisely.settings import SECRET_KEY, ALGORITHMS
from .models         import User

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = jwt.decode(request.headers['Authorization'], SECRET_KEY, algorithms = ALGORITHMS)
            request.user = User.objects.get(id = access_token['id'])
            return func(self, request, *args, **kwargs)
        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'USER_DOES_NOT_EXIST'}, status = 400)
    return wrapper
