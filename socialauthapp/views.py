from django.shortcuts import render_to_response
from django.template.context import RequestContext

import json
import oauth2
import requests

def home(request):
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user, })
   if request.user.is_authenticated():
       #social_user = request.user.social_auth.filter(provider='twitter',).first()
       if request.user.social_auth.filter(provider='twitter',).first():
           friends = json.loads(oauth_req( 'https://api.twitter.com/1.1/friends/list.json', '294900602-wzPWDkIx6quWgVvoibpNSLYpvv8sOUCl00vr9HbJ', 'xsU46EFIyqd84Rp8f4Lh5HAMVlsMXVnAzL3yEOqDYirae' ))
           context['twfriends'] = friends['users']
           return render_to_response("home.html", context_instance = context)
       if  request.user.social_auth.filter(provider='google-oauth2',).first():
           social = request.user.social_auth.get(provider='google-oauth2')
           response = requests.get('https://www.googleapis.com/plus/v1/people/me/people/visible', params={'access_token': social.extra_data['access_token']})
           context['goofriends'] = response.json()['items']
           return render_to_response("home.html", context_instance = context)
            
   return render_to_response('home.html', context_instance=context)

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key='esLCGMC9I29NljN00nKlm97Qq', secret='nUcjPP7IJ8zKoQoINY1u6VIcW9fq2Cg7s4HT8UwioVdgD5c1FZ')
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content
    
#need "sudo pip install oauth2" or "sudo pip easy_install oauth2" 
def twfriends(request):
    friends = json.loads(oauth_req( 'https://api.twitter.com/1.1/friends/list.json', '294900602-wzPWDkIx6quWgVvoibpNSLYpvv8sOUCl00vr9HbJ', 'xsU46EFIyqd84Rp8f4Lh5HAMVlsMXVnAzL3yEOqDYirae' ))
    return render_to_response("home.html",{'twfriends':friends['users'],}) 
    
def goofriends(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://www.googleapis.com/plus/v1/people/me/people/visible',
        params={'access_token': social.extra_data['access_token']}
    )
    print(response.json())
    friends = response.json()['items']
    return render_to_response("home.html",{'goofriends':friends,}) 
                            