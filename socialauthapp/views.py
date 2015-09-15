from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.conf import settings

import json
import oauth2
import requests

def home(request):
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user, })
   if request.user.is_authenticated():
       if request.user.social_auth.filter(provider='twitter',).first():
           social = request.user.social_auth.get(provider='twitter')
           friends = json.loads(oauth_req( 'https://api.twitter.com/1.1/friends/list.json', social.extra_data['access_token']['oauth_token'], social.extra_data['access_token']['oauth_token_secret']))
           context['twfriends'] = friends['users']
           return render_to_response("home.html", context_instance = context)
       # Get google friends: https://python-social-auth.readthedocs.org/en/latest/use_cases.html#retrieve-google-friends
       if  request.user.social_auth.filter(provider='google-oauth2',).first():
           social = request.user.social_auth.get(provider='google-oauth2')
           response = requests.get('https://www.googleapis.com/plus/v1/people/me/people/visible', params={'access_token': social.extra_data['access_token']})
           context['goofriends'] = response.json()['items']
           return render_to_response("home.html", context_instance = context)
            
   return render_to_response('home.html', context_instance=context)

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=settings.SOCIAL_AUTH_TWITTER_KEY, secret=settings.SOCIAL_AUTH_TWITTER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content