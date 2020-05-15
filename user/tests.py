import json

import bcrypt

from .models          import User

from django.test      import TestCase
from django.test      import Client
from unittest.mock    import patch, MagicMock

class EmailCheckTest(TestCase):
    def setUp(self):
        User.objects.create(
            email = 'test@gmail.com',
            name  = '와이즐리'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_emailCheck_post_login(self):
        client = Client()
        user = {'email' : 'test@gmail.com'}
        response = client.post('/check', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
             {'data' :
             {'name' : '와이즐리', 'message' : 'EMAIL_EXISTS'}})

    def test_emailCheck_post_account(self):
        client = Client()
        user = {'email' : 'test1@gmail.com'}
        response = client.post('/check', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {'message' : 'EMAIL_DO_NOT_EXISTS'})

    def test_emailCheck_post_key_error(self):
        client = Client()
        user = {'emal': 'test@gmail.com'}
        response = client.post('/check', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
             {'message' : 'KEY_ERROR'})

class SignUpTest(TestCase):
    def setUp(self):
         User.objects.create(
            email         = 'test1@test.com',
            password      =  bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            phone         = '010-3333-4444',
            birth         = '2020-05-14',
            name          = '위즐리',
            gender        = '남자',
            alarm_confirm = 1
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_success(self):
        client = Client()
        signup = {
            'email'         : 'test2@test.com',
            'password'      :  bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'phone'         : '010-5558-5555',
            'birth'         : '2020-05-14',
            'name'          : '와아이',
            'gender'        : '여자',
            'alarm_confirm' : 1
        }

        response = client.post('/signup', json.dumps(signup), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_signup_key_error(self):
        client = Client()
        signup = {
            'emai'          : 'test2@test.com',
            'password'      :  bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'phone'         : '010-5558-5555',
            'birth'         : '2020-05-14',
            'name'          : '와아이',
            'gender'        : '여자',
            'alarm_confirm' : 1
        }

        response = client.post('/signup', json.dumps(signup), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
             {'message' : 'KEY_ERROR'}
        )

class LoginTest(TestCase):
    def setUp(self):
        User.objects.create(
        email    = 'test@test.com',
        password = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
    def tearDown(self):
        User.objects.all().delete()

    def test_login_success(self):
        client = Client()
        user = 'test@test.com'
        login = {'email' : 'test@test.com', 'password' : '1234'}
        response = client.post('/login', json.dumps(login), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {'access_token' : response.json()['access_token']})

    def test_login_fail(self):
        client = Client()
        user = 'test@test.com'
        login = {'email' : 'test@test.com', 'password' : '1235'}
        response = client.post('/login', json.dumps(login), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_key_error(self):
        client = Client()
        user = 'test@test.com'
        login = {'mail' : 'test@test.com', 'password' : '1235'}
        response = client.post('/login', json.dumps(login), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
             {'message' : 'KEY_ERROR'}
        )

