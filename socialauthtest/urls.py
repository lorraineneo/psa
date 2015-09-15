from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    
    url(r'^$', 'socialauthapp.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^goofriends/$', 'socialauthapp.views.goofriends'),
    url(r'^twfriends/$', 'socialauthapp.views.twfriends'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
)
