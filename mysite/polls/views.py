from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from random import randint
from django.contrib.auth.decorators import login_required
from polls.models import ExcersiseTemplate, Replacers, NameForm, templates, AnotherForm, ChoiseForm, Primer, TemplateForm, SavedPrimer,  makeNicePdf
from .models import Question, Choice, Primer, NameForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def index(request):
    teacher_check = request.user.groups.filter(name='Учитель').exists()
    context = {
        'teacher_check': teacher_check
    }
    return render(request, 'mysite/lms.html', context)


@login_required
def home(request):
    teacher_check = request.user.groups.filter(name='Учитель').exists()
    numberOfTemplatesUser = 0
    stroka = []
    check = ''

    x = templates(check)
    if request.method == 'POST':
        numberOfTemplates = NameForm(request.POST)
        if numberOfTemplates.is_valid():
            numberOfTemplatesUser = numberOfTemplates.cleaned_data['your_name']
            stroka = []
            for i in range(int(numberOfTemplatesUser)):
                y = templates()
                stroka.append('Название задачи:\n' + str(y[2])+'\n \n' + 'Задача:\n' + str(y[0])+'\n \n' + 'Ответ:\n'+str(y[1])+'\n')
                print(stroka)
    else:
        numberOfTemplates = NameForm()

    context = {
        'teacher_check': teacher_check,
        'groups': request.user.groups.all(),
        'text': x[0],
        'answer': x[1],
        'name': x[2],
        'number': numberOfTemplates,
        'numberUser': numberOfTemplatesUser,
        'stroka': stroka
    }

    return render(request, 'mysite/home.html', context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def primer(request):
    ch = (randint(1,10))
    chh = (randint(1,10))
    summm = ch+chh
    p = Primer (sl = str(ch),sll = str(chh),summ = str(summm),znak = '+')
    teacher_check = request.user.groups.filter(name='Учитель').exists()
    summmm = 0
    check = ''
    answerCheck = 'Вы еще не ввели ответ'
    if request.method == 'POST':
        form = AnotherForm(request.POST)


        if form.is_valid():
            summmm = form.cleaned_data['field']
            print (summmm,'не из бд',p.summ)
            summa = Primer.objects.last()
            print ('из БД',summa.summ)
            if int(summmm) == int(summa.summ):
                answerCheck = True
            else:
                answerCheck = False



    else:
        form = AnotherForm()

        answerCheck = 'Вы еще не ввели ответ'
    Primer.objects.all().delete()
    p.save()
    return render(request, 'polls/primer.html', {'teacher_check' : teacher_check,
            'sl': p.sl,
            'sll': p.sll,'znak' : p.znak,'form' : form, 'number' : summmm, 'answerCheck' : answerCheck,  'check' : check})




    
    

