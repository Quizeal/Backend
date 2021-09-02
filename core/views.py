from core.models import QuizAnswered, QuizDetails, QuizMarks, QuizOptions, Questions
from django.contrib.auth.models import User
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

import jwt
from Quizeal.settings import SIMPLE_JWT


def generate_quiz_token():
    unique = False

    while not unique:
        res = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not QuizDetails.objects.filter(quiz_token=res).exists():
            unique = True

    return res


def custom_sort(dict):
    return dict["marks"]


class VerifyToken:
    """
    Verify Token
    """

    def has_permission(self, request, view):
        token = request.headers["Authorization"].split(" ")[1]
        decode = jwt.decode(
            token,
            SIMPLE_JWT["SIGNING_KEY"],
            algorithms=[SIMPLE_JWT["ALGORITHM"]],
        )

        if not decode:
            return False

        user = User.objects.get(id=decode["user_id"])

        if not user:
            return False

        if user.username != view.kwargs.get("username"):
            return False

        return True


class CreateQuiz(APIView):
    permission_classes = [IsAuthenticated, VerifyToken]

    def post(self, request, username):
        option_list = []
        question_list = []
        total_marks = 0

        for question in request.data["questions"]:

            for option in question["options"]:
                optionSerializer = serializers.QuizOptionsSerializer(data=option)

                if optionSerializer.is_valid():
                    optionInstance = optionSerializer.save()
                    option_list.append(optionInstance.pk)

                else:
                    return Response(
                        {"status": 500, "detail": optionSerializer.errors}, status=500
                    )

            question["options"] = option_list
            questionsSerializer = serializers.QuestionsSerializer(data=question)
            total_marks += question["question_marks"]

            if questionsSerializer.is_valid():
                questionInstance = questionsSerializer.save()
                question_list.append(questionInstance.pk)

            else:
                return Response(
                    {"status": 500, "detail": questionsSerializer.errors}, status=500
                )

            option_list.clear()

        request.data["username"] = username
        request.data["questions"] = question_list
        request.data["total_marks"] = total_marks
        request.data["quiz_token"] = generate_quiz_token()
        quizDetailsSerializer = serializers.QuizDetailsSerializer(data=request.data)

        if quizDetailsSerializer.is_valid():
            quizDetailsSerializer.save()
        else:
            return Response(
                {"status": 500, "detail": quizDetailsSerializer.errors}, status=500
            )

        return Response(
            {
                "status": 200,
                "detail": "Quiz created successfully",
                "data": quizDetailsSerializer.data,
            }
        )


class SubmitQuiz(APIView):

    permission_classes = [IsAuthenticated, VerifyToken]

    def post(self, request, username, quiz_token):

        intz = pytz.timezone("Asia/Kolkata")

        try:
            quiz_details_qs = QuizDetails.objects.get(quiz_token=quiz_token)

        except:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        quiz_id = quiz_details_qs.pk

        quiz_datetime = datetime.combine(
            quiz_details_qs.date, quiz_details_qs.start_time
        )
        quiz_datetime = intz.localize(quiz_datetime)
        quiz_end_datetime = quiz_datetime + quiz_details_qs.duration
        quiz_end_datetime += timedelta(minutes=6)

        if quiz_end_datetime < datetime.now(intz):
            return Response(
                {"status": 404, "detail": "Quiz has already ended"}, status=404
            )

        if QuizMarks.objects.filter(username=username, quiz_id=quiz_id).exists():
            return Response(
                {
                    "status": 404,
                    "detail": "Quiz has already been submitted by this user",
                },
                status=404,
            )

        questions_qs = quiz_details_qs.questions.all().prefetch_related("options")
        marks = 0
        total_marks = 0
        option_list = []

        response = request.data["answers"]

        for i in range(len(response)):

            response[i]["quiz_id"] = quiz_id
            response[i]["username"] = username
            quizAnsweredSerializer = serializers.QuizAnsweredSerializer(
                data=response[i]
            )

            if quizAnsweredSerializer.is_valid():
                quizAnsweredSerializer.save()
            else:
                return Response(
                    {"status": 500, "detail": quizAnsweredSerializer.errors}, status=500
                )

            option_list.append(response[i]["option_name"])

            if (
                i == len(response) - 1
                or response[i]["question_id"] != response[i + 1]["question_id"]
            ):

                question = questions_qs.get(pk=response[i]["question_id"])
                # options_qs = QuizOptions.objects.filter(question_id_id = response[i]["question_id"],is_correct = True)

                options_qs = question.options.filter(is_correct=True)

                total_marks += question.question_marks
                correct_ans = True

                if len(option_list) != len(options_qs):
                    correct_ans = False

                for option in option_list:
                    if not options_qs.filter(option_name=option).exists():
                        correct_ans = False

                if correct_ans:
                    marks += question.question_marks

                option_list.clear()

        quiz_marks = QuizMarks(
            marks=marks,
            total_marks=total_marks,
            quiz_id=quiz_details_qs,
            username=username,
        )
        quiz_marks.save()

        return Response(
            {
                "status": 200,
                "detail": "Quiz has been submitted successfully!",
                "marks": str(marks) + "/" + str(quiz_details_qs.total_marks),
            }
        )


class GetQuiz(APIView):

    permission_classes = [IsAuthenticated, VerifyToken]

    def get(self, request, username, quiz_token):

        intz = pytz.timezone("Asia/Kolkata")

        try:
            quiz_details_qs = QuizDetails.objects.prefetch_related("questions").get(
                quiz_token=quiz_token, is_active=True
            )
        except:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        quiz_id = quiz_details_qs.pk

        if QuizMarks.objects.filter(username=username, quiz_id=quiz_id).exists():
            return Response(
                {
                    "status": 404,
                    "detail": "Quiz has already been submitted by this user",
                },
                status=404,
            )

        quiz_datetime = datetime.combine(
            quiz_details_qs.date, quiz_details_qs.start_time
        )
        quiz_datetime = intz.localize(quiz_datetime)
        quiz_end_datetime = quiz_datetime + quiz_details_qs.duration

        if quiz_datetime > datetime.now(intz):
            return Response(
                {"status": 404, "detail": "Quiz not started yet!"}, status=404
            )

        if quiz_end_datetime < datetime.now(intz):
            return Response(
                {"status": 404, "detail": "Quiz has already ended!"}, status=404
            )

        quiz_details = model_to_dict(quiz_details_qs)
        quiz_details["questions"] = []
        questions_qs = quiz_details_qs.questions.all().prefetch_related("options")

        for question in questions_qs:
            quiz_details["questions"].append(model_to_dict(question))

            quiz_details["questions"][-1]["options"] = []
            options = question.options.all()

            for option in options:
                quiz_details["questions"][-1]["options"].append(model_to_dict(option))
                del quiz_details["questions"][-1]["options"][-1]["is_correct"]
                del quiz_details["questions"][-1]["options"][-1]["is_active"]

        return Response({"status": 200, "data": quiz_details})


class ViewQuiz(APIView):

    permission_classes = [IsAuthenticated, VerifyToken]

    def get(self, request, username, quiz_token):

        try:
            quiz_details_qs = QuizDetails.objects.prefetch_related("questions").get(
                quiz_token=quiz_token
            )

        except:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        if not quiz_details_qs.is_active:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        if quiz_details_qs.username != username:
            return Response({"status": 401, "detail": "Not Authorized"}, status=401)

        quiz_details = model_to_dict(quiz_details_qs)
        quiz_details["questions"] = []
        questions_qs = quiz_details_qs.questions.all().prefetch_related("options")

        for question in questions_qs:
            quiz_details["questions"].append(model_to_dict(question))

            quiz_details["questions"][-1]["options"] = []
            options = question.options.all()

            for option in options:
                quiz_details["questions"][-1]["options"].append(model_to_dict(option))
                del quiz_details["questions"][-1]["options"][-1]["is_active"]

        return Response({"status": 200, "data": quiz_details})


class QuizReport(APIView):

    permission_classes = [IsAuthenticated, VerifyToken]

    def get(self, request, username, quiz_token):

        try:
            quiz_details_qs = QuizDetails.objects.prefetch_related("questions").get(
                quiz_token=quiz_token
            )
        except:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        try:
            User.objects.get(username=username)
        except:
            return Response(
                {"status": 404, "detail": "User does not exist"}, status=404
            )

        if not quiz_details_qs.is_active:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        quiz_id = quiz_details_qs.pk
        marks_qs = QuizMarks.objects.filter(quiz_id=quiz_id)

        if not marks_qs.filter(username=username).exists():
            return Response(
                {"status": 404, "detail": "User has not attempted the quiz"}, status=404
            )

        quiz_details = model_to_dict(quiz_details_qs)
        quiz_details["questions"] = []
        questions_qs = quiz_details_qs.questions.all().prefetch_related("options")
        quiz_answered_qs = QuizAnswered.objects.filter(quiz_id=quiz_id)

        intz = pytz.timezone("Asia/Kolkata")
        quiz_datetime = datetime.combine(
            quiz_details_qs.date, quiz_details_qs.start_time
        )
        quiz_datetime = intz.localize(quiz_datetime)
        quiz_end_datetime = quiz_datetime + quiz_details_qs.duration
        quiz_end_datetime += timedelta(minutes=6)

        if quiz_end_datetime > datetime.now(intz):
            return Response(
                {"status": 404, "detail": "Quiz has not yet ended"}, status=404
            )

        for question in questions_qs:
            quiz_details["questions"].append(model_to_dict(question))

            quiz_details["questions"][-1]["options"] = []
            options = question.options.all()

            for option in options:
                quiz_details["questions"][-1]["options"].append(model_to_dict(option))

                quiz_details["questions"][-1]["options"][-1]["is_marked"] = False

                if quiz_answered_qs.filter(
                    option_name=option.option_name, question_id=question.id
                ).exists():
                    quiz_details["questions"][-1]["options"][-1]["is_marked"] = True

                del quiz_details["questions"][-1]["options"][-1]["is_active"]

        marks_list = []
        user_rank = 1
        user_marks = 0
        total_marks = 0

        for marks in marks_qs:
            marks_list.append(marks.marks)
            if marks.username == username:
                user_marks = marks.marks
                total_marks = marks.total_marks

        marks_list.sort(reverse=True)

        for marks in marks_list:
            if marks != user_marks:
                user_rank += 1
            else:
                break

        top_10_percentile_list = marks_list[: len(marks_list) // 10]

        if len(top_10_percentile_list) > 0:
            quiz_details["top_10_percentile"] = sum(top_10_percentile_list) / len(
                top_10_percentile_list
            )
        else:
            quiz_details["top_10_percentile"] = 0

        quiz_details["average"] = sum(marks_list) / len(marks_list)
        quiz_details["total_students"] = len(marks_list)
        quiz_details["topper_marks"] = marks_list[0]
        quiz_details["user_marks"] = user_marks
        quiz_details["user_rank"] = user_rank
        quiz_details["total_marks"] = total_marks

        return Response({"status": 200, "data": quiz_details})


class MyQuizes(APIView):

    permission_classes = [IsAuthenticated, VerifyToken]

    def get(self, request, username):

        try:
            User.objects.get(username=username)
        except:
            return Response(
                {"status": 404, "detail": "User does not exist"}, status=404
            )

        my_quizes = {"created": [], "attempted": []}

        created_quiz_qs = QuizDetails.objects.filter(username=username, is_active=True)

        for quiz in created_quiz_qs:
            my_quizes["created"].append(model_to_dict(quiz))

        attempted_quiz_qs = QuizMarks.objects.filter(
            username=username, is_active=True
        ).select_related("quiz_id")

        for quiz in attempted_quiz_qs:
            my_quizes["attempted"].append(
                {**model_to_dict(quiz), **model_to_dict(quiz.quiz_id)}
            )

        return Response(
            {"status": 200, "data": my_quizes},
        )


class QuizResult(APIView):

    permission_classes = [IsAuthenticated, VerifyToken]

    def get(self, request, username, quiz_token):

        try:
            quiz_details_qs = QuizDetails.objects.prefetch_related("questions").get(
                quiz_token=quiz_token
            )
        except:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        if not quiz_details_qs.is_active:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        try:
            User.objects.get(username=username)
        except:
            return Response(
                {"status": 404, "detail": "user does not exist"}, status=404
            )

        quiz_id = quiz_details_qs.pk
        marks_qs = QuizMarks.objects.filter(quiz_id=quiz_id)

        quiz_result = model_to_dict(quiz_details_qs)
        student_list = []

        for marks in marks_qs:
            student = {}
            user = User.objects.get(username=marks.username)
            student["id"] = user.id
            student["name"] = user.first_name + " " + user.last_name
            student["username"] = user.username
            student["email"] = user.email
            student["marks"] = marks.marks
            student_list.append(student)

        sorted(student_list, key=custom_sort, reverse=True)

        if len(student_list):
            student_list[0]["rank"] = 1
            for i in range(1, len(student_list)):

                if student_list[i]["marks"] == student_list[i - 1]["marks"]:
                    student_list[i]["rank"] = student_list[i - 1]["rank"]
                else:
                    student_list[i]["rank"] = i + 1

        quiz_result["students"] = student_list

        return Response({"status": 200, "data": quiz_result})


class deleteCreated(APIView):
    permission_classes = [IsAuthenticated, VerifyToken]

    def get(self, request, quiz_token, username):
        try:
            qs = QuizDetails.objects.get(quiz_token=quiz_token, username=username)
        except:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        if not qs.is_active:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        qs.is_active = False
        qs.save()
        return Response({"status": 200, "data": "Quiz Deleted Successfully"})


class deleteAttempted(APIView):
    permission_classes = [IsAuthenticated, VerifyToken]

    def get(self, request, username, quiz_token):

        try:
            quiz_qs = QuizDetails.objects.get(quiz_token=quiz_token)
            quizmarks_qs = QuizMarks.objects.get(quiz_id=quiz_qs.id, username=username)

        except:
            return Response(
                {"status": 404, "detail": "Invalid credentials"}, status=404
            )

        if not quizmarks_qs.is_active:
            return Response(
                {"status": 404, "detail": "Quiz does not exist"}, status=404
            )

        quizmarks_qs.is_active = False
        quizmarks_qs.save()
        return Response({"status": 200, "data": "Quiz Deleted Successfully"})


# todo
# Currently delete attempted quiz behavious is NOT OK.
