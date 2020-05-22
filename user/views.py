import json
import bcrypt
import jwt

from django.views    import View
from django.http     import HttpResponse, JsonResponse

from .models         import User
from wisely.settings import SECRET_KEY

class EmailCheckView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email = data['email']).exists():
               user = User.objects.get(email=data['email'])
               data = {
                        'name'    : user.name,
                        'message' : 'EMAIL_EXISTS'
               }
               return JsonResponse({'data' : data}, status = 200)
            return JsonResponse({'message' : 'EMAIL_DO_NOT_EXISTS'}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            User.objects.create(
                email         = data['email'],
                password      = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                phone         = data['phone'],
                birth         = data['birth'],
                name          = data['name'],
                gender        = data['gender'],
                alarm_confirm = data['alarm_confirm']
            )
            return JsonResponse({'message' : 'SUCCESS'},status = 200)
        except KeyError:
           return JsonResponse({'message':'KEY_ERROR'}, status = 400)

class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = User.objects.get(email = data['email'])
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
               token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = 'HS256')
               return JsonResponse({'access_token' : token.decode('utf-8')}, status=200)
            return HttpResponse(status = 400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

