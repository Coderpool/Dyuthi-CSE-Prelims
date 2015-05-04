# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from exam.models import Set,Questions,Event,Score
from random import shuffle
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control

def is_a_volunteer(user):
    if user.groups.filter(name='volunteer').count() == 1 :
        return True
    return False


@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def test(request):
    questions = []
    arg = {}
    if request.method == 'POST':
        event = Event.objects.filter(name = request.POST['event'])[0]
        score_obj = Score.objects.filter(user = request.user,event = event)[0]
        if score_obj.startTime is None:
            score_obj.startTime = datetime.now()
            score_obj.save()
            sets = Set.objects.filter(test = event)
            for i in sets:
                setquestions = Questions.objects.filter(set = i).order_by('?')[:i.numberOfQuestions]
                for j in  setquestions:
                    options = [j.answer,j.option_B,j.option_C,j.option_D]
                    shuffle(options)
                    question = {"question":j.question,"id":j.id,"options":options}
                    questions.append(question)
            arg['questions'] = questions
            arg['event'] = event.eventId
            arg['time'] = event.durationInMins
            return render_to_response('exam/test.html',arg,context_instance=RequestContext(request))
    return HttpResponseRedirect('/home')



def evaluate(request):
    if request.method == 'POST':
        answers = []
        score = 0
        negative = 0
        score_obj = Score.objects.filter(user = request.user,event = int(request.POST['event']))[0]
        score_obj.score=0
        delta  = datetime.now()-score_obj.startTime
        for i in request.POST:
            if i == 'csrfmiddlewaretoken' or i == 'event':
                continue
            try:
                question = Questions.objects.filter(id=i)[0]
                if request.POST[i] =='leavethequestion':
                    pass
                elif question.answer == request.POST[i]:
                    score = score + question.set.positiveMarks
                else :
                    score = score - question.set.negativeMarks
                    negative = negative + 1
            except:
                pass
        score_obj.score = score
        score_obj.negatives = negative
        score_obj.deltaSec = delta.seconds
        score_obj.deltaMicro = delta.microseconds
        score_obj.save()
        return HttpResponseRedirect('/home?message=Test Submitted Successfully')




@login_required
@user_passes_test(lambda u:is_a_volunteer(u))
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def leaderboard(request):
    try :
        event = Event.objects.filter(name = request.GET['event'])[0]
        leaders=Score.objects.filter(event=event,score__isnull=False).order_by('-score','negatives','deltaSec','deltaMicro')
        arg = {}
        arg['event']=event
        arg['leaders']=leaders
        return render_to_response('exam/leaderboard.html',arg,context_instance=RequestContext(request))
    except:
        events = Event.objects.all()
        return render_to_response('exam/eventselect.html',locals(),context_instance=RequestContext(request))
