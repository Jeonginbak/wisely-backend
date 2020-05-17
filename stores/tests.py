import json

from django.test    import TestCase, Client

from product.models import RazorSet, Color, RazorSetImage
from .models        import Cart

class RazorCartTest(TestCase):
    def setUp(self):
        navy_color = Color.objects.create(
            id = 1,
            name = '미드나이트 네이비',
            code = '#00306b'
        )

        razor_image = RazorSetImage.objects.create(
            id = 1,
            product_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/starter_kit/starter_navy.png',
            result_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_razor_navy.png',
            color = navy_color
        )

        RazorSet.objects.create(
            id = 1,
            price = 8900,
            image = razor_image
        )

    def tearDown(self):
        Color.objects.all().delete()
        RazorSetImage.objects.all().delete()
        RazorSet.objects.all().delete()

    def test_razor_cart_post_success(self):
        client = Client()
        navy_razor = { "color_id" : "1" }
        response = client.post('/razor-set/cart', json.dumps(navy_razor), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_razor_cart_post_add_quantity_success(self):
        client = Client()
        navy_razor = { "color_id" : "1" }
        response = client.post('/razor-set/cart', json.dumps(navy_razor), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_razor_cart_post_not_found(self):
        client = Client()
        navy_razor = { "color_id" : "4" }
        response = client.post('/razor-set/cart', json.dumps(navy_razor), content_type = 'application/json')
        self.assertEqual(response.json(), {
            'message' : 'PRODUCT_DOES_NOT_EXIST'
        })
        self.assertEqual(response.status_code, 400)

    def test_razor_cart_post_key_error(self):
        client = Client()
        navy_razor = { "color" : "4" }
        response = client.post('/razor-set/cart', json.dumps(navy_razor), content_type = 'application/json')
        self.assertEqual(response.json(), {
            'message' : 'KEY_ERROR'
        })
        self.assertEqual(response.status_code, 400)
