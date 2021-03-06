from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from random import randint, shuffle
from .helper import get_seconds_from_string, get_string_from_seconds
from django.contrib.auth.decorators import login_required
from .models import Exercise, TrainingTest, TrainingApparatus
from .serializers import TrainingTestSerializer
from polls.models import Exercise
from account.models import Account
from control.models import ControlTest
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
    control_tests = ControlTest.objects.all().values_list('id', flat=True)
    is_control = False
    if test.id in control_tests:
        is_control = True
    context = {
        'is_control': is_control,
        'test_description': test.apparatus.description,
    }
    return render(request, 'polls/primer.html', context)


def create_test(request):
    print(request.body)
    req = json.loads(request.body)
    apparatus = TrainingApparatus.objects.get(name=req['trainingApparatus'])
    user = Account.objects.get(pk=request.user.id)
    if req['testType'] == 'training':
        test = TrainingTest(apparatus=apparatus, user=user, grade=0)
    elif req['testType'] == 'control':
        test = ControlTest(apparatus=apparatus, user=user, grade=0)
    test.time_start = datetime.datetime.now()
    test.save()
    unsolved_exercises = []
    if apparatus.name == "Разложение второго слагаемого":
        first = [2, 3, 4, 5, 6, 7, 8, 9]
        second = [9, 8, 7, 6, 5, 4, 3, 2]
        for fn in first:
            for sn in second:
                if fn + sn >= 11:
                    result = fn + sn
                    excess_value = result - 10
                    correct_answer = (str(sn-(sn-excess_value)) + '+' + str(sn-excess_value)).replace("'",'')
                    unsolved_exercise = Exercise(test=test, type=apparatus.exercises_type, time_spent=None, correct_answer=correct_answer,
                                                 given_answer='', answer_is_correct=False, text=str(fn) + '+' + str(sn))
                    unsolved_exercises.append(unsolved_exercise)
        shuffle(unsolved_exercises)
        unsolved_exercises[:apparatus.exercises_amount]
        for ex in unsolved_exercises:
            exercise_index = unsolved_exercises.index(ex) + 1
            ex.exercise_index = exercise_index
            ex.save()

    elif apparatus.name == "Разложение первого слагаемого":
        first = [2, 3, 4, 5, 6, 7, 8, 9]
        second = [9, 8, 7, 6, 5, 4, 3, 2]
        for fn in first:
            for sn in second:
                if fn + sn >=11:
                    result = fn + sn
                    excess_value = result - 10
                    correct_answer = f"{fn-(fn-excess_value)}+{fn-excess_value}".replace("'",'')
                    unsolved_exercise = Exercise(test=test, type=apparatus.exercises_type, time_spent=None, correct_answer=correct_answer,
                                                 given_answer='', answer_is_correct=False, text=f"{fn} + {sn}")
                    unsolved_exercises.append(unsolved_exercise)
        shuffle(unsolved_exercises)
        unsolved_exercises[:apparatus.exercises_amount]
        for ex in unsolved_exercises:
            exercise_index = unsolved_exercises.index(ex) + 1
            ex.exercise_index = exercise_index
            ex.save()
    elif apparatus.name == "Сложение":
        first = [2, 3, 4, 5, 6, 7, 8, 9]
        second = [9, 8, 7, 6, 5, 4, 3, 2]
        for fn in first:
            for sn in second:
                if fn + sn >= 11:
                    result = fn + sn
                    unsolved_exercise = Exercise(test=test, type=apparatus.exercises_type, time_spent=None, correct_answer=str(result),
                                                 given_answer='', answer_is_correct=False, text=f"{fn} + {sn}")
                    unsolved_exercises.append(unsolved_exercise)
        shuffle(unsolved_exercises)
        unsolved_exercises[:apparatus.exercises_amount]
        for ex in unsolved_exercises:
            exercise_index = unsolved_exercises.index(ex) + 1
            ex.exercise_index = exercise_index
            ex.save()
    elif apparatus.name == "Разложение вычитаемого":
        first = [18, 17, 16, 15, 14, 13, 12, 11]
        second = [2, 3, 4, 5, 6, 7, 8, 9]
        for fn in first:
            for sn in second:
                if fn - sn <= 9:
                    result = fn - sn
                    excess_value = fn - 10
                    correct_answer = f"{excess_value}+{sn - excess_value}".replace("'", "")
                    unsolved_exercise = Exercise(test=test, type=apparatus.exercises_type, time_spent=None, correct_answer=correct_answer,
                                                 given_answer='', answer_is_correct=False, text=f"{fn} - {sn}")
                    unsolved_exercises.append(unsolved_exercise)
        shuffle(unsolved_exercises)
        unsolved_exercises[:apparatus.exercises_amount]
        for ex in unsolved_exercises:
            exercise_index = unsolved_exercises.index(ex) + 1
            ex.exercise_index = exercise_index
            ex.save()
    return JsonResponse({
        'status': 'ok'
    })


def get_exercise(request):
    test = TrainingTest.objects.filter(user_id=request.user.id).last()
    test.solved_exercises = test.exercises.filter(time_spent__isnull=False).count()
    exercise_index = test.solved_exercises + 1
    test.save()
    print('test time spent', get_string_from_seconds(datetime.datetime.now().timestamp() - test.time_start.timestamp()))
    time_spent = round(datetime.datetime.now().timestamp() - test.time_start.timestamp())
    if exercise_index <= test.apparatus.exercises_amount and time_spent <= get_seconds_from_string(test.apparatus.allotted_time):
        unsolved_exercise = test.exercises.filter(exercise_index=exercise_index)[0]
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
    correct_answers = test.exercises.filter(answer_is_correct=True).count()
    solved_exercises = test.exercises.filter(time_spent__isnull=False)
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
    if not test.time_spent:
        test.time_spent = get_string_from_seconds(time_spent)
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

    control_tests = ControlTest.objects.all().values_list('id', flat=True) #fixme: need rework
    is_control = False
    if test.id in control_tests:
        is_control = True
    context = {
        "is_control": is_control,
        "time_spent": test.time_spent,
        "correct_answers": correct_answers,
        'exercises_amount': test.apparatus.exercises_amount,
        "correct_answers_percentage": correct_answers_percentage,
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
    exercise.time_spent = str(datetime.datetime.fromtimestamp(req['time_spent']).time()).split('.')[0]
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


def stats(request):
    context = {
        'tests': TrainingApparatus.objects.all()
    }
    return render(request, 'mysite/stats.html', context)


def get_stats(request):
    req = json.loads(request.body)
    tests = TrainingTest.objects.filter(user_id=request.user.id, apparatus__name=req['trainingApparatus'],
                                        time_spent__isnull=False)
    serializer = TrainingTestSerializer(tests, many=True)
    return JsonResponse({
        'tests': serializer.data,
    })
    
    
