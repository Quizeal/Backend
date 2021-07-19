from core.models import QuizDetails
from django.shortcuts import render
from . import serializers
from django.http import JsonResponse

#third party imports
from rest_framework.response import Response
from rest_framework.views import APIView

class CreateQuiz(APIView):

    def post(self,request,*args,**kwargs):

        quizDetailsSerializer = serializers.QuizDetailsSerializer(data = request.data)
        
        if quizDetailsSerializer.is_valid():
            quizInstance = quizDetailsSerializer.save()
            #return Response(quizDetailsSerializer.data)

        else:
            return Response(quizDetailsSerializer.errors)

        for question in request.data["questions"]:
            question['quiz_id'] = quizInstance.pk
            questionsSerializer = serializers.QuestionsSerializer(data = question)
                
            if questionsSerializer.is_valid():
                questionInstance = questionsSerializer.save()

            else:
                #print(questionsSerializer.quiz_id)
                return Response(questionsSerializer.errors)

            for option in question["options"]:
                option['question_id'] = questionInstance.pk
                optionSerializer = serializers.QuizOptionsSerializer(data = option)

                if optionSerializer.is_valid():
                    optionInstance = optionSerializer.save()
                    #print(optionInstance)
                
                else:
                    return Response(optionSerializer.errors)

        return JsonResponse({'data':"Succesfully completed request!"})
        

class SubmitQuiz(APIView):

    def post(self,request,*args,**kwargs):
        

        for response in request.data['answers']:
            quizAnsweredSerializer = serializers.QuizAnsweredSerializer(data = response)
            
            if quizAnsweredSerializer.is_valid():
                    quizAnsweredInstance = quizAnsweredSerializer.save()
                    print(quizAnsweredInstance)
                
            else:
                return Response(quizAnsweredSerializer.errors)

        return JsonResponse({'data':"Succesfully completed request!"})