from core.models import QuizDetails, QuizOptions, Questions
from django.shortcuts import render
from . import serializers
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime
from datetime import timedelta
import pytz

#third party imports
from rest_framework.response import Response
from rest_framework.views import APIView

# class CreateQuiz(APIView):

#     def post(self,request,*args,**kwargs):

#         quizDetailsSerializer = serializers.QuizDetailsSerializer(data = request.data)
      
#         if quizDetailsSerializer.is_valid():
#             quizInstance = quizDetailsSerializer.save()
#             #return Response(quizDetailsSerializer.data)

#         else:
#             return Response(quizDetailsSerializer.errors)

#         for question in request.data["questions"]:
#             question['quiz_id'] = quizInstance.pk
#             questionsSerializer = serializers.QuestionsSerializer(data = question) 
                
#             if questionsSerializer.is_valid():
#                 questionInstance = questionsSerializer.save()

#             else:
#                 #print(questionsSerializer.quiz_id)
#                 return Response(questionsSerializer.errors)

#             for option in question["options"]:
#                 option['question_id'] = questionInstance.pk
#                 optionSerializer = serializers.QuizOptionsSerializer(data = option)

#                 if optionSerializer.is_valid():
#                     optionInstance = optionSerializer.save()
#                     #print(optionInstance)
                
#                 else:
#                     return Response(optionSerializer.errors)

#         return Response(quizDetailsSerializer.data)
        


class CreateQuiz(APIView):

    def post(self,request,*args,**kwargs):

        option_list = []
        question_list = []

        for question in request.data["questions"]:

            for option in question["options"]:
                    optionSerializer = serializers.QuizOptionsSerializer(data = option)

                    if optionSerializer.is_valid():
                        optionInstance = optionSerializer.save()
                        option_list.append(optionInstance.pk)
                        #print(optionInstance)
                    
                    else:
                        return Response(optionSerializer.errors)

            question['options'] = option_list
            questionsSerializer = serializers.QuestionsSerializer(data = question)
                
            if questionsSerializer.is_valid():
                questionInstance = questionsSerializer.save()
                question_list.append(questionInstance.pk)

            else:
                #print(questionsSerializer.quiz_id)
                return Response(questionsSerializer.errors)

        request.data['questions'] = question_list
        quizDetailsSerializer = serializers.QuizDetailsSerializer(data = request.data)
      
        if quizDetailsSerializer.is_valid():
            quizDetailsInstance = quizDetailsSerializer.save()
            #return Response(quizDetailsSerializer.data)

        else:
            return Response(quizDetailsSerializer.errors)      

        return Response(quizDetailsSerializer.data)


class SubmitQuiz(APIView):

    def post(self,request,*args,**kwargs):
        
        intz = pytz.timezone('Asia/Kolkata')

        question_id = request.data['answers'][0]['question_id']
        question = Questions.objects.get(pk = question_id)

        quiz_details_qs = QuizDetails.objects.get(pk = question.quiz_details.pk)

        quiz_datetime = datetime.combine(quiz_details_qs.date, quiz_details_qs.start_time)
        quiz_datetime = quiz_datetime.replace(tzinfo = intz)
        quiz_end_datetime = quiz_datetime + quiz_details_qs.duration
        quiz_end_datetime = quiz_end_datetime.replace(tzinfo = intz)
        
        quiz_end_datetime += timedelta(minutes=6)
        
        print(quiz_datetime)
        print(datetime.now(intz))
        print(quiz_end_datetime)
        
        if datetime.now(intz) > quiz_end_datetime:
            return JsonResponse({"msg":"Quiz has ended. Cannot submit now!"})

        for response in request.data['answers']:

            quizAnsweredSerializer = serializers.QuizAnsweredSerializer(data = response)
 
            if quizAnsweredSerializer.is_valid():
                    quizAnsweredInstance = quizAnsweredSerializer.save()
                    #print(quizAnsweredInstance)
                
            else:
                return Response(quizAnsweredSerializer.errors)

        return Response(quizAnsweredSerializer.data)


class GetQuiz(APIView):

    def get(self,request,*args,**kwargs):

        intz = pytz.timezone('Asia/Kolkata')
        quiz_details_qs = QuizDetails.objects.prefetch_related('questions').get(id = request.data["quiz_id"])
        quiz_datetime = datetime.combine(quiz_details_qs.date, quiz_details_qs.start_time)
        quiz_datetime = quiz_datetime.replace(tzinfo = intz)
        quiz_end_datetime = quiz_datetime + quiz_details_qs.duration
        quiz_end_datetime = quiz_end_datetime.replace(tzinfo = intz)

        print(quiz_datetime)
        print(datetime.now(intz))
        print(quiz_end_datetime)
        
        if quiz_end_datetime > datetime.now(intz):
            return JsonResponse({"msg" : "Quiz has already ended!"})

        if quiz_datetime < datetime.now(intz):
            return JsonResponse({"msg" : "Quiz not started yet!"})

        
        quiz_details = model_to_dict(quiz_details_qs)
        quiz_details["questions"] = []
        questions_list = quiz_details_qs.questions

        print(questions_list)
        questions_qs = Questions.objects.filter(quiz_details = request.data["quiz_id"]).prefetch_related('options')


        for question in questions_qs:
            quiz_details["questions"].append(model_to_dict(question))
 
        for question in quiz_details["questions"]:
            options_qs = QuizOptions.objects.only("option_name").filter(id = question['id'])

            question["options"] = []

            for option in options_qs:
                question["options"].append(model_to_dict(option))
                del question["options"][-1]["is_correct"]
                del question["options"][-1]["is_active"]

        return JsonResponse(quiz_details)