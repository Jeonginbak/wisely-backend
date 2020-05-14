import json

from django.test import TestCase, Client

from .models     import Question, Answer

class QuestionTest(TestCase):
    def setUp(self):
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
          "question": "얼마나 자주 면도하세요?",
          "answers": [
            {
              "answer": "하루에 여러 번",
              "description": "하루에 여러 번 면도 한다면 날은 1주마다 교체해 주세요."
            },
            {
              "answer": "하루에 한 번",
              "description": "하루에 한 번 면도 한다면 날은 2주마다 교체해 주세요."
            },
            {
              "answer": "2~3일에 한 번",
              "description": "2~3일에 한 번 면도 한다면 날은 4주마다 교체해 주세요."
            }
          ]
        })
        self.assertEqual(response.status_code, 200)

    def test_question_get_not_found(self):
        client = Client()
        response = client.get('/subscription-survey/6')
        self.assertEqual(response.json(), {
          'message' : 'QUESTION_DOES_NOT_EXIST'
        })
        self.assertEqual(response.status_code, 400)
