from django.conf.urls import patterns, url, include
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from dyuthicseprelims.settings import STATIC_ROOT
admin.autodiscover()

urlpatterns = patterns('',

     url(r'^$','login.views.default'),
     url(r'^login$','login.views.userlogin'),
     url(r'^logout$','login.views.userlogout'),
     url(r'^home$','login.views.home'),
     url(r'^adduser$','regdesk.views.adduser'),
     url(r'^deskhome$','regdesk.views.home'),
     url(r'^user_exist$','regdesk.views.userExist'),
     url(r'^test$','exam.views.test'),
     url(r'^evaluate$','exam.views.evaluate'),
     url(r'^leaderboard$','exam.views.leaderboard'),
     url(r'^volhome$','volunteer.views.home'),
     url(r'^addquestion$','volunteer.views.addQuestion'),
     url(r'^edit$','volunteer.views.edit'),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)




urlpatterns += patterns('',
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT, 'show_indexes' : True}),
)