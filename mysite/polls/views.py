from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from random import randint
from .helper import get_seconds_from_string, get_string_from_seconds
from django.contrib.auth.decorators import login_required
from .models import Exercise, NameForm, TrainingTest, TrainingApparatus
from django.contrib.auth.models import User
from polls.models import Exercise
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import datetime


@login_required
def index(request):
    context = {
        'tests': TrainingApparatus.objects.all()
    }
    return render(request, 'mysite/lms.html', context)


def get_allotted_time(request):
    test = TrainingTest.objects.filter(user_id=request.user.id).last()
    return JsonResponse({
        "allotted_time": get_seconds_from_string(test.apparatus.allotted_time),
        "url": "/end_test/",
        "test_id": test.id
    })

def exercise_view(request):
    test = TrainingTest.objects.filter(user_id=request.user.id).last()
    context = {
        'test_description': test.apparatus.description,
    }
    return render(request, 'polls/primer.html', context)


def create_test(request):
    print(request.body)
    req = json.loads(request.body)
    apparatus = TrainingApparatus.objects.get(name=req['trainingApparatus'])
    user = User.objects.get(pk=request.user.id)
    test = TrainingTest(apparatus=apparatus, user=user, grade=0)
    test.time_start = datetime.datetime.now()
    test.save()
    unsolved_exercises = []
    if apparatus.name == "Разложение второго слагаемого":
        for i in range(1, apparatus.exercises_amount+1):
            ch = (randint(2, 9))
            chh = (randint(11-ch, 9))
            znak = '+'
            result = ch+chh
            excess_value = result - 10
            exercise_index = i
            correct_answer = (str(chh-(chh-excess_value)) + '+' + str(chh-excess_value)).replace("'", '')
            unsolved_exercise = Exercise(test=test, type=apparatus.exercises_type, time_spent=None, correct_answer=correct_answer,
                                         given_answer='', answer_is_correct=False, text=str(ch) + str(znak) + str(chh),
                                         exercise_index=exercise_index)
            unsolved_exercise.save()
            unsolved_exercises.append(unsolved_exercise.pk)
    else:
        for i in range(1, apparatus.exercises_amount+1):
            ch = (randint(2, 9))
            chh = (randint(11-ch, 9))
            znak = '+'
            result = ch+chh
            excess_value = result - 10
            exercise_index = i
            correct_answer = (str(ch-(ch-excess_value)) + '+' + str(ch-excess_value)).replace("'", '')
            unsolved_exercise = Exercise(test=test, type=apparatus.exercises_type, time_spent=None, correct_answer=correct_answer,
                                         given_answer='', answer_is_correct=False, text=str(ch) + str(znak) + str(chh),
                                         exercise_index=exercise_index)
            unsolved_exercise.save()
            unsolved_exercises.append(unsolved_exercise.pk)
    return JsonResponse({
        'status': 'ok'
    })


def get_exercise(request):
    test = TrainingTest.objects.filter(user_id=request.user.id).last()
    test.solved_exercises = test.exercise_set.filter(time_spent__isnull=False).count()
    exercise_index = test.solved_exercises + 1
    test.save()
    print('test time spent', get_string_from_seconds(datetime.datetime.now().timestamp() - test.time_start.timestamp()))
    time_spent = round(datetime.datetime.now().timestamp() - test.time_start.timestamp())
    if exercise_index <= test.apparatus.exercises_amount and time_spent <= get_seconds_from_string(test.apparatus.allotted_time):
        unsolved_exercise = test.exercise_set.filter(exercise_index=exercise_index)[0]
    else:
        return JsonResponse({
            "url": "/end_test/",
            "test_id": test.id
        })
    return JsonResponse({
        'text': unsolved_exercise.text,
        'pk': unsolved_exercise.pk,
        'test_id': unsolved_exercise.test.id,
        'exercise_index': unsolved_exercise.exercise_index
    })


def end_test_id(request, test_id):
    test = TrainingTest.objects.get(id=int(test_id))
    correct_answers = test.exercise_set.filter(answer_is_correct=True).count()
    solved_exercises = test.exercise_set.filter(time_spent__isnull=False)
    exercises_amount = test.apparatus.exercises_amount
    correct_answers_percentage = correct_answers/exercises_amount*100
    if correct_answers_percentage >= test.apparatus.perfect:
        grade = 5
    elif correct_answers_percentage >= test.apparatus.good:
        grade = 4
    elif correct_answers_percentage >= test.apparatus.satisfactory:
        grade = 3
    else:
        grade = 2
    test.grade = grade
    test.solved_exercises = solved_exercises.count()
    test.correct_answers = correct_answers
    time_spent = round(datetime.datetime.now().timestamp() - test.time_start.timestamp())
    print ('time spent in seconds', time_spent)
    # print('asasas', get_string_from_seconds(time_spent))
    if not test.time_spent:
        test.time_spent = get_string_from_seconds(time_spent)
        print('dssdsd', test.time_spent)
    test.save()


    history = []
    print(test.apparatus.exercises_amount)
    for exercise in solved_exercises:
        solved_exercise = {
            'text': exercise.text,
            'pk': exercise.pk,
            'is_correct': exercise.answer_is_correct,
            'correct_answer': exercise.correct_answer,
            'given_answer': exercise.given_answer,
            'time_spent': exercise.time_spent
        }
        history.append(solved_exercise)


    context = {
        "time_spent": test.time_spent,
        "correct_answers": correct_answers,
        'exercises_amount': test.apparatus.exercises_amount,
        "correct_answers_percentage": str(correct_answers_percentage) + "%",
        "grade": grade,
        "history": history
    }
    return render(request, 'mysite/results.html', context)


def check_answer(request):
    req = json.loads(request.body)
    exercise = Exercise.objects.get(pk=req['pk'])
    exercise.given_answer = req['value']
    exercise.exercise_index = req['exercise_index']
    test = TrainingTest.objects.filter(user_id=request.user.id).last()
    exercise.time_spent = datetime.datetime.fromtimestamp(req['time_spent'])
    if str(exercise.given_answer) != '' and exercise.given_answer == exercise.correct_answer:
        is_correct = True
    else:
        is_correct = False
    print(is_correct, str(exercise.given_answer), exercise.correct_answer)
    exercise.answer_is_correct = is_correct
    exercise.save()
    test.save()
    return JsonResponse({
        'is_correct': is_correct
    }, safe=False)


def get_history(request):
    req = json.loads(request.body)
    history = []
    try:
        solved_exercises = Exercise.objects.filter(test=req['test_id'], time_spent__isnull=False)
        for exercise in solved_exercises:
            solved_exercise = {
                'text': exercise.text,
                'pk': exercise.pk,
                'is_correct': exercise.answer_is_correct,
                'correct_answer': exercise.correct_answer,
                'given_answer': exercise.given_answer,
                'time_spent': exercise.time_spent
            }
            history.append(solved_exercise)
    except KeyError:
        pass
    return JsonResponse(
        history, safe=False
    )

@login_required
def home1(request):
    id = request.user.id
    idHome = "/home/" + str(request.user.id)
    if id == None:
        idHome = '/login/'
    return HttpResponseRedirect(idHome)


# def end_test(request):
#     test = TrainingTest.objects.filter(user_id=request.user.id).last()
#     correct_answers = test.correct_answers
#     exercises_amount = test.apparatus.exercises_amount
#     correct_answers_percentage = correct_answers/exercises_amount*100
#     if correct_answers_percentage >= test.apparatus.perfect:
#         grade = 5
#     elif correct_answers_percentage >= test.apparatus.good:
#         grade = 4
#     elif correct_answers_percentage >= test.apparatus.satisfactory:
#         grade = 3
#     else:
#         grade = 2
#     test.grade = grade
#     test.save()
#     context = {
#         "time_spent": test.time_spent,
#         "correct_answers": correct_answers,
#         "correct_answers_percentage": str(correct_answers_percentage) + "%",
#         "grade": grade,
#     }
#     return render(request, 'mysite/results.html', context)

    
    

