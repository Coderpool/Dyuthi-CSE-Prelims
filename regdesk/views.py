# Create your views here.
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import Group
from exam.models import Event,Score
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.shortcuts import render_to_response

def is_a_regdesk(user):
	if user.groups.filter(name='regdesk').count() == 1 :
		return True
	return False

@login_required
@user_passes_test(lambda u:is_a_regdesk(u))
@cache_control(no_cache=True, must_revalidate=True,no_store=True)

def home(request):
	events = Event.objects.all()
	return render_to_response('regdesk/regdeskhome.html',locals(), context_instance = RequestContext(request))


@login_required
@user_passes_test(lambda u:is_a_regdesk(u))
@cache_control(no_cache=True, must_revalidate=True,no_store=True)

def adduser(request):
	e = {}
	if request.method == 'POST':
		user = User.objects.create_user(request.POST['username'],'',request.POST['password'])
		grp = Group.objects.get(name = 'participant')
		grp.user_set.add(user)
		user.save()
		events = Event.objects.all()
		for event in events:
			try:
				if request.POST[str(event.eventId)] == 'on':
					Score.create(user,event).save()	
					e.append(event.eventId)
			except:
				pass
		message = "User added successfully";
		return render_to_response('regdesk/regdeskhome.html',locals(), context_instance = RequestContext(request))


def userExist(request):
	try:
		if User.objects.filter(username=request.GET['user']).count() == 0:
			return HttpResponse('5')
		else:
			return HttpResponse('0')
	except:
		return HttpResponse('9'); 
