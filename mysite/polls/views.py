from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from random import randint
from polls.models import ExcersiseTemplate, Replacers, NameForm, Primer, AnotherForm



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
                answerCheck = 'Правильно'
            else:
                answerCheck = 'Неправильно'



    else:
        form = AnotherForm()

        answerCheck = 'Вы еще не ввели ответ'
    Primer.objects.all().delete()
    p.save()
    return render(request, 'polls/primer.html', {
            'sl': p.sl,
            'sll': p.sll,'znak' : p.znak,'form' : form, 'number' : summmm, 'answerCheck' : answerCheck,  'check' : check})




    
    

