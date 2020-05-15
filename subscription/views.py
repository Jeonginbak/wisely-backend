import json

from django.http          import JsonResponse
from django.views         import View
from subscription.models  import Question, Answer

class SurveyView(View):
    def get(self, request, question_id):
        try:
            question = Question.objects.prefetch_related('answer_set').get(id = question_id)

            data = [{
                'answer'      : answer.answer,
                'description' : answer.description,
            } for answer in question.answer_set.all()]

            return JsonResponse({'question' : question.question, 'answers' : data}, status = 200)

        except Question.DoesNotExist:
            return JsonResponse({'message' : 'QUESTION_DOES_NOT_EXIST'}, status = 400)
