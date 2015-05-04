# Create your views here.
from exam.models import Questions,Set
from django.template import RequestContext
from volunteer.models import Volunteer
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
def is_a_volunteer(user):
	if user.groups.filter(name='volunteer').count() == 1 :
		return True
	return False
@login_required
@user_passes_test(lambda u:is_a_volunteer(u))
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def home(request):
	event = Volunteer.objects.filter(user = request.user)[0]
	sets = Set.objects.filter(test = event.event)
	return render_to_response('volunteer/volhome.html',locals(), context_instance = RequestContext(request))
def addQuestion(request):
	if request.method == 'POST':
		set = Set.objects.filter(setId = request.POST['set'])[0]
		question = Questions.create(request.POST['question'],request.POST['answer'],request.POST['optionB'],request.POST['optionC'],request.POST['optionD'],set)
		question.save()
		arg={}
		if request.POST['formname'] =='editform':
			arg['message']= "Question added successfully"
			return HttpResponseRedirect('/edit')
		else:
			arg['message']= "Question added successfully"
			return HttpResponseRedirect('/home')
@login_required
@user_passes_test(lambda u:is_a_volunteer(u))
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def edit(request):
	event = Volunteer.objects.filter(user = request.user)[0]
	sets = Set.objects.filter(test = event.event)
	if request.method == 'GET':
		arg = {}
		questionset = {}
		for i in sets:
			questionset.update({i.setname:Questions.objects.filter(set = i)})
		arg['questionset']=questionset
		return render_to_response('volunteer/showall.html',arg, context_instance = RequestContext(request))
	elif request.method == 'POST':
		question = Questions.objects.filter(id = request.POST['id'])[0]
		arg = {}
		arg['question'] = question
		arg['sets']=sets
		question.delete();
		return render_to_response('volunteer/edit.html',arg, context_instance = RequestContext(request))
