from core.models import QuizAnswered, QuizDetails, QuizMarks, QuizOptions, Questions
from . import serializers
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime
from datetime import timedelta
import pytz
import string
import random

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

def generate_quiz_token():
        unique = False

        while not unique:
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
            if not QuizDetails.objects.filter(quiz_token = res).exists():
                unique = True

        return res

class CreateQuiz(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):

        option_list = []
        question_list = []
        total_marks = 0

        for question in request.data["questions"]:

            for option in question["options"]:
                    optionSerializer = serializers.QuizOptionsSerializer(data = option)

                    if optionSerializer.is_valid():
                        optionInstance = optionSerializer.save()
                        option_list.append(optionInstance.pk)

                    else:
                        return Response(optionSerializer.errors)

            question["options"] = option_list
            questionsSerializer = serializers.QuestionsSerializer(data = question)
            total_marks+=question["question_marks"]
                
            if questionsSerializer.is_valid():
                questionInstance = questionsSerializer.save()
                question_list.append(questionInstance.pk)

            else:
                #print(questionsSerializer.quiz_id)
                return Response(questionsSerializer.errors)
        
            option_list.clear()

        request.data['questions'] = question_list
        request.data['total_marks'] = total_marks
        request.data['quiz_token'] = generate_quiz_token()
        quizDetailsSerializer = serializers.QuizDetailsSerializer(data = request.data)

        if quizDetailsSerializer.is_valid():
            quizDetailsSerializer.save()
        else:
            return Response(quizDetailsSerializer.errors)

        return Response(quizDetailsSerializer.data)


class SubmitQuiz(APIView):

    permission_classes = [IsAuthenticated]
    def post(self,request,quiz_token):

        intz = pytz.timezone('Asia/Kolkata')

        quiz_details_qs = QuizDetails.objects.get(quiz_token = quiz_token)
        quiz_id = quiz_details_qs.pk

        quiz_datetime = datetime.combine(quiz_details_qs.date, quiz_details_qs.start_time)
        quiz_datetime = intz.localize(quiz_datetime)
        quiz_end_datetime = quiz_datetime + quiz_details_qs.duration
        quiz_end_datetime += timedelta(minutes=6)

        print(quiz_end_datetime)
        print(datetime.now(intz))

        if quiz_end_datetime<datetime.now(intz):
            return JsonResponse({"msg" : "Quiz has already ended"})

        if QuizMarks.objects.filter(username = request.data["username"],quiz_id = quiz_id).exists():
            return JsonResponse({"msg" : "Quiz has already been submitted by this user"})

        questions_qs = quiz_details_qs.questions.all().prefetch_related('options') 
        marks = 0
        total_marks = 0
        option_list = []

        response = request.data['answers']

        for i in range(len(response)):

            response[i]["quiz_id"] = quiz_id
            response[i]["username"] = request.data["username"]
            quizAnsweredSerializer = serializers.QuizAnsweredSerializer(data = response[i])
 
            if quizAnsweredSerializer.is_valid():
                    quizAnsweredSerializer.save()
                    #print(quizAnsweredInstance)
        
            else:
                return Response(quizAnsweredSerializer.errors)

            option_list.append(response[i]["option_name"])

            if i==len(response)-1 or response[i]["question_id"] != response[i+1]["question_id"]:

                question = questions_qs.get(pk=response[i]["question_id"])
                # options_qs = QuizOptions.objects.filter(question_id_id = response[i]["question_id"],is_correct = True)

                options_qs = question.options.filter(is_correct = True)

                total_marks += question.question_marks           
                correct_ans = True
                
                print(option_list)

                if len(option_list) != len(options_qs):
                    correct_ans = False

                for option in option_list:
                    if not options_qs.filter(option_name = option).exists():
                        correct_ans = False
                    
                if correct_ans:
                    marks += question.question_marks

                option_list.clear()


        quiz_marks = QuizMarks(marks = marks, total_marks = total_marks, quiz_id = quiz_details_qs, username = request.data["username"])
        quiz_marks.save()

        return JsonResponse({"msg" : "Quiz has been submitted successfully!", "marks" : str(marks) + "/"+ str(total_marks)})


class GetQuiz(APIView):

    permission_classes = [IsAuthenticated]
    def get(self,request,quiz_token):

        intz = pytz.timezone('Asia/Kolkata')
        quiz_details_qs = QuizDetails.objects.prefetch_related('questions').get(quiz_token = quiz_token)
        quiz_datetime = datetime.combine(quiz_details_qs.date, quiz_details_qs.start_time)
        quiz_datetime = intz.localize(quiz_datetime)
        quiz_end_datetime = quiz_datetime + quiz_details_qs.duration

        if quiz_datetime > datetime.now(intz):
            return JsonResponse({"msg" : "Quiz not started yet!"})
        
        if quiz_end_datetime < datetime.now(intz):
            return JsonResponse({"msg" : "Quiz has already ended!"})

        quiz_details = model_to_dict(quiz_details_qs)
        quiz_details["questions"] = []
        questions_qs = quiz_details_qs.questions.all().prefetch_related('options')


        for question in questions_qs:
            quiz_details["questions"].append(model_to_dict(question))

            quiz_details["questions"][-1]["options"] = []
            options = question.options.all()

            for option in options:
                quiz_details["questions"][-1]["options"].append(model_to_dict(option))
                del quiz_details["questions"][-1]["options"][-1]["is_correct"]
                del quiz_details["questions"][-1]["options"][-1]["is_active"]

        return JsonResponse(quiz_details)

class ViewQuiz(APIView):

    permission_classes = [IsAuthenticated]
    def get(self,request,quiz_token):

        quiz_details_qs = QuizDetails.objects.prefetch_related('questions').get(quiz_token = quiz_token)
        quiz_details = model_to_dict(quiz_details_qs)
        quiz_details["questions"] = []
        questions_qs = quiz_details_qs.questions.all().prefetch_related('options')

    
        for question in questions_qs:
            quiz_details["questions"].append(model_to_dict(question))

            quiz_details["questions"][-1]["options"] = []
            options = question.options.all()

            for option in options:
                quiz_details["questions"][-1]["options"].append(model_to_dict(option))
                del quiz_details["questions"][-1]["options"][-1]["is_active"]

        return JsonResponse(quiz_details)


class QuizReport(APIView):

    permission_classes = [IsAuthenticated]
    def post(self,request,quiz_token):   
        
        quiz_details_qs = QuizDetails.objects.prefetch_related('questions').get(quiz_token = quiz_token)
        quiz_id = quiz_details_qs.pk

        marks_qs = QuizMarks.objects.filter(quiz_id = quiz_id)
        quiz_details = model_to_dict(quiz_details_qs)
        quiz_details["questions"] = []
        questions_qs = quiz_details_qs.questions.all().prefetch_related('options')
        quiz_answered_qs = QuizAnswered.objects.filter(quiz_id = quiz_id)

        intz = pytz.timezone('Asia/Kolkata')
        quiz_datetime = datetime.combine(quiz_details_qs.date, quiz_details_qs.start_time)
        quiz_datetime = intz.localize(quiz_datetime)
        quiz_end_datetime = quiz_datetime + quiz_details_qs.duration
        quiz_end_datetime += timedelta(minutes=6)

        if quiz_end_datetime>datetime.now(intz):
            return JsonResponse({"msg" : "Quiz has not yet ended"})

        # print(quiz_answered_qs.values_list())

        for question in questions_qs:
            quiz_details["questions"].append(model_to_dict(question))

            quiz_details["questions"][-1]["options"] = []
            options = question.options.all()

            for option in options:
                quiz_details["questions"][-1]["options"].append(model_to_dict(option))

                quiz_details["questions"][-1]["options"][-1]["is_marked"] = False

                if quiz_answered_qs.filter(answer_name = option.option_name, question_id = question.id).exists():
                    quiz_details["questions"][-1]["options"][-1]["is_marked"] = True

                del quiz_details["questions"][-1]["options"][-1]["is_active"]

        marks_list = []
        user_rank = 1

        for marks in marks_qs:
            marks_list.append(marks.marks)
            if marks.username == request.data["username"]:
                user_marks = marks.marks
                total_marks = marks.total_marks

        marks_list.sort(reverse=True)

        for marks in marks_list:
            if marks!=user_marks:
                user_rank+=1
            else:
                break

        quiz_details["average"] = sum(marks_list)/len(marks_list)
        quiz_details["total_students"] = len(marks_list)
        quiz_details["topper_marks"] = marks_list[0]
        quiz_details["user_marks"] = user_marks
        quiz_details["user_rank"] = user_rank
        quiz_details["total_marks"] = total_marks
                  
        return JsonResponse(quiz_details)


class MyQuizes(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,username):

        my_quizes = {"created":[],"attempted":[]}

        created_quiz_qs = QuizDetails.objects.filter(username = username)

        for quiz in created_quiz_qs:
            my_quizes["created"].append(model_to_dict(quiz))

        attempted_quiz_qs = QuizMarks.objects.filter(username = username).select_related('quiz_id')

        for quiz in attempted_quiz_qs:
            my_quizes["attempted"].append({**model_to_dict(quiz), **model_to_dict(quiz.quiz_id)})
            
        return JsonResponse(my_quizes)
