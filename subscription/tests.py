import json

from django.test   import TestCase, Client

from .models       import Question, Answer
from stores.models import (
    Color,
    GiftSet,
    GiftSetImage,
    RazorSetImage,
    RazorSet,
    Blade,
    ShavingGel,
    AfterShave,
    AfterShaveSkinType,
    SkinType,
    RazorImages
)

class QuestionTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        question_1 = Question.objects.create(
            id = 1,
            question = '얼마나 자주 면도하세요?'
        )

        Answer.objects.create(
            answer = '하루에 여러 번',
            description = '하루에 여러 번 면도 한다면 날은 1주마다 교체해 주세요.',
            question = question_1
        )

        Answer.objects.create(
            answer = '하루에 한 번',
            description = '하루에 한 번 면도 한다면 날은 2주마다 교체해 주세요.',
            question = question_1
        )

        Answer.objects.create(
            answer = '2~3일에 한 번',
            description = '2~3일에 한 번 면도 한다면 날은 4주마다 교체해 주세요.',
            question = question_1
        )

    def test_question_get_success(self):
        client = Client()
        response = client.get('/subscription-survey/1')
        self.assertEqual(response.json(), {
        'data': {
            'question': '얼마나 자주 면도하세요?',
            'answers': [
                '하루에 여러 번',
                '하루에 한 번',
                '2~3일에 한 번'
            ],
            "description": [
                '하루에 여러 번 면도 한다면 날은 1주마다 교체해 주세요.',
                '하루에 한 번 면도 한다면 날은 2주마다 교체해 주세요.',
                '2~3일에 한 번 면도 한다면 날은 4주마다 교체해 주세요.'
              ]
            }
        })
        self.assertEqual(response.status_code, 200)

    def test_question_get_not_found(self):
        client = Client()
        response = client.get('/subscription-survey/6')
        self.assertEqual(response.json(), {
          'message' : 'QUESTION_DOES_NOT_EXIST'
        })
        self.assertEqual(response.status_code, 400)

class ResultTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        navy_color = Color.objects.create(
            id   = 1,
            name = '미드나이트 네이비',
            code = '#00306b'
        )
        gift_image = GiftSetImage.objects.create(
            id = 1,
            product_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/gift_set/gift_set_navy.png',
            color = navy_color
        )
        gift_set_navy = GiftSet.objects.create(
            id = 1,
            name  = '선물세트(면도용품+기프트 카드)',
            price = 29800,
            image = gift_image
        )
        razor_image = RazorSetImage.objects.create(
            id = 1,
            product_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/starter_kit/starter_navy.png',
            result_image  = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_razor_navy.png',
            color         = navy_color
        )
        RazorSet.objects.create(
            id    = 1,
            name = '면도기세트(면도기+날2입)',
            price = 8900,
            image = razor_image
        )
        Blade.objects.create(
            id = 1,
            name =  '리필면도날 (4입)',
            price = 9600,
            image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/blade/refill_blade.png',
            result_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_blade.png'
        )
        ShavingGel.objects.create(
            id   = 1,
            name = '스탠다드 150ml',
            price = 4500,
            image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/shaving_gel/shaving_gel_150.png',
            result_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_gel.png'
        )
        after_shave_60ml = AfterShave.objects.create(
            id    = 1,
            name  = '스탠다드 60ml',
            price = 6500
        )
        after_shave_30ml = AfterShave.objects.create(
            id    = 2,
            name  = '여행용 30ml',
            price = 3900
        )
        skin_type_dry = SkinType.objects.create(
            id   = 2,
            name = '건성'
        )
        skin_type_oily = SkinType.objects.create(
            id   = 1,
            name = '지성'
        )
        after_shave_60ml_dry = AfterShaveSkinType.objects.create(
            id = 2,
            after_shave  = after_shave_60ml,
            skin_type    = skin_type_dry,
            image        = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/aftershaving/after_shaving_gel_dry_60.png',
            result_image = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_after_shaving_gel.png'
        )
        after_shave_30ml_oily = AfterShaveSkinType.objects.create(
            id = 3,
            after_shave = after_shave_30ml,
            skin_type   = skin_type_oily,
            image       = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/starter_aftershaveing/after_shaving_gel_oily_30.png'
        )

        RazorImages.objects.create(
            image_type = 'zero_up',
            image      = 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/razor_0up/zero_up_navy.png',
            color      = navy_color
        )

    def tearDown(self):
        Color.objects.all().delete()
        GiftSetImage.objects.all().delete()
        GiftSet.objects.all().delete()
        RazorSetImage.objects.all().delete()
        RazorSet.objects.all().delete()
        Blade.objects.all().delete()
        ShavingGel.objects.all().delete()
        AfterShave.objects.all().delete()
        SkinType.objects.all().delete()
        AfterShaveSkinType.objects.all().delete()

    def test_survey_result_success(self):
      client = Client()
      cart = {
              'answer_1' : '1',
              'answer_2' : '2',
              'answer_3' : '1',
              'answer_4' : '1'
            }
      response = client.post('/subscription-result', json.dumps(cart), content_type = 'application/json')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.json(),{
        'image': {
        'razor_image': 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_razor_navy.png',
        'blade_image': 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_blade.png',
        'shaving_gel_image': 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_gel.png',
        'sub_image': [
            {
                'image': 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/items/razor_0up/zero_up_navy.png'
            }
        ],
            'after_shave_image': 'https://wiselyshave-cdn.s3.amazonaws.com/assets/images/surveyResult/survey_result_after_shaving_gel.png'
        },
        'product': {
            'razor': {
                'name': '면도기세트(면도기+날2입)',
                'price': 8900,
                'color': '미드나이트 네이비'
            },
            'blade': {
                'name': '리필면도날 (4입)',
                'price': 9600
            },
            'shaving_gel': {
                'name': '스탠다드 150ml',
                'price': 4500
            },
            'after_shave': {
                'name': '스탠다드 60ml',
                'price': 6500
            }
          }})

    def test_survey_result_key_error(self):
        client = Client()
        cart = {
                'answer_1' : '1',
                'answer'   : '2',
                'answer_3' : '1',
                'answer_4' : '1'
                }
        response = client.post('/subscription-result', json.dumps(cart), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{"message": "KEY_ERROR"})
