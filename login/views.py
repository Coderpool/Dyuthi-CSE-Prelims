# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from exam.models import Event

def default(request):
	if request.user.is_authenticated() :
		return HttpResponseRedirect('/home');
	return render_to_response('login/login.html', context_instance = RequestContext(request))

def userlogin(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home');
	if request.method == 'POST':
		user = authenticate(username = request.POST['username'],password = request.POST['password'])
		if user is not None:
			login(request,user)
			return HttpResponseRedirect('/home')
	return render_to_response('login/login.html',{'message' : 'Wrong Username or Password'},context_instance =RequestContext(request))


@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def home(request):
	arg={}
	if request.user.groups.filter(name='participant').count() == 1:
		try:
			arg['message']=request.GET['message']
		except:
			pass
		events = Event.objects.filter(score__user = request.user,score__startTime__isnull=True)
		if events.count() > 0:
			arg['events']=events
			return render_to_response('login/userhome.html',arg,context_instance = RequestContext(request))
		else:
			return render_to_response('login/finished.html',arg,context_instance = RequestContext(request))
	elif request.user.groups.filter(name='regdesk').count() == 1:
		return HttpResponseRedirect('/deskhome')	
	elif request.user.groups.filter(name='volunteer').count() == 1:
		return HttpResponseRedirect('/volhome')	
	else:
		return HttpResponseRedirect('/admin')
def userlogout(request):
	logout(request)
	return HttpResponseRedirect('/')
