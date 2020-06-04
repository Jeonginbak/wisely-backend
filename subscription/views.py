import json

from django.http          import JsonResponse
from django.views         import View
from subscription.models  import Question, Answer
from stores.models        import (
    RazorSet,
    Blade,
    ShavingGel,
    AfterShaveSkinType,
    RazorImages
)

class SurveyView(View):
    def get(self, request, question_id):
        try:
            question = Question.objects.prefetch_related('answer_set').get(id = question_id)

            data = {
                'question'    : question.question,
                'answers'     : [answer.answer for answer in question.answer_set.all()],
                'description' : [answer.description for answer in question.answer_set.all()]
            }

            return JsonResponse({'data' : data}, status = 200)
        except Question.DoesNotExist:
            return JsonResponse({'message' : 'QUESTION_DOES_NOT_EXIST'}, status = 400)

class ResultView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            razor = (
                RazorSet
                .objects
                .select_related('image', 'image__color')
                .get(image__color_id = data['color_id'])
            )
            blade       = Blade.objects.get(type = 'regular')
            shaving_gel = ShavingGel.objects.first(type = 'regular')
            image       = {
                'razor_image'       : razor.image.result_image,
                'blade_image'       : blade.result_image,
                'shaving_gel_image' : shaving_gel.result_image,
                'sub_image'         : list(RazorImages.objects.filter(color_id = data['color_id'], image_type = 'zero_up').values('image'))
            }
            products = {
                'razor' : {
                    'name'  : razor.name,
                    'price' : razor.price,
                    'color' : razor.image.color.name
                },
                'blade' : {
                    'name'  : blade.name,
                    'price' : blade.price
                },
                'shaving_gel' : {
                    'name'  : shaving_gel.name,
                    'price' : shaving_gel.price
                }
            }

            if data['after_shave']:
                after_shave = (
                    AfterShaveSkinType
                    .objects
                    .select_related('after_shave')
                    .get(skin_type = data['skin_type'], type = 'regular')
                )

                image['after_shave_image'] = after_shave.result_image
                products['after_shave']    = {
                    'name'  : after_shave.after_shave.name,
                    'price' : after_shave.after_shave.price,
                }
            return JsonResponse({'image' : image, 'product' : products}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
