from core.models import QuizAnswered, QuizDetails, QuizMarks, QuizOptions, Questions
from . import serializers
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import datetime
from datetime import timedelta
import pytz


from rest_framework.response import Response
from rest_framework.views import APIView
        

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

                    else:
                        return Response(optionSerializer.errors)

            question["options"] = option_list
            questionsSerializer = serializers.QuestionsSerializer(data = question)
                
            if questionsSerializer.is_valid():
                questionInstance = questionsSerializer.save()
                question_list.append(questionInstance.pk)

            else:
                #print(questionsSerializer.quiz_id)
                return Response(questionsSerializer.errors)
        
            option_list.clear()

        request.data['questions'] = question_list
        quizDetailsSerializer = serializers.QuizDetailsSerializer(data = request.data)
      
        if quizDetailsSerializer.is_valid():
            quizDetailsInstance = quizDetailsSerializer.save()
            #return Response(quizDetailsSerializer.data)

        else:
            return Response(quizDetailsSerializer.errors)      

        return Response(quizDetailsSerializer.data)


class SubmitQuiz(APIView):

    def post(self,request,quiz_id):
        
        intz = pytz.timezone('Asia/Kolkata')

        quiz_details_qs = QuizDetails.objects.get(pk = quiz_id)

        quiz_datetime = datetime.combine(quiz_details_qs.date, quiz_details_qs.start_time)
        quiz_datetime = intz.localize(quiz_datetime)
        quiz_end_datetime = quiz_datetime + quiz_details_qs.duration
        quiz_end_datetime += timedelta(minutes=6)


        questions_qs = quiz_details_qs.questions.all().prefetch_related('options') 
        marks = 0
        total_marks = 0
        option_list = []

        response = request.data['answers']

        for i in range(len(response)):

            response[i]["quiz_id"] = quiz_id
            quizAnsweredSerializer = serializers.QuizAnsweredSerializer(data = response[i])
 
            if quizAnsweredSerializer.is_valid():
                    quizAnsweredInstance = quizAnsweredSerializer.save()
                    #print(quizAnsweredInstance)
        
            else:
                return Response(quizAnsweredSerializer.errors)

            option_list.append(response[i]["answer_name"])

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


        quiz_marks = QuizMarks(marks = marks, total_marks = total_marks, quiz_id = quiz_details_qs)
        quiz_marks.save()
        

        return JsonResponse({"msg" : "Quiz has been submitted successfully!", "marks" : str(marks) + "/"+ str(total_marks)})


class GetQuiz(APIView):

    def get(self,request,quiz_id):

        intz = pytz.timezone('Asia/Kolkata')
        quiz_details_qs = QuizDetails.objects.prefetch_related('questions').get(id = quiz_id)
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

    def get(self,request,quiz_id):

        quiz_details_qs = QuizDetails.objects.prefetch_related('questions').get(id = quiz_id)
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

    def get(self,request,quiz_id):   
        
        
        marks_qs = QuizMarks.objects.get(quiz_id = quiz_id)

        quiz_details_qs = QuizDetails.objects.prefetch_related('questions').get(id = quiz_id)
        quiz_details = model_to_dict(quiz_details_qs)
        quiz_details["questions"] = []
        questions_qs = quiz_details_qs.questions.all().prefetch_related('options')
        quiz_answered_qs = QuizAnswered.objects.filter(quiz_id = quiz_id)

        print(quiz_answered_qs.values_list())

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


        return JsonResponse(quiz_details)

