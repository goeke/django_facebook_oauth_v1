import urllib

from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

import urllib
import urllib2
from facebook.models import FacebookProfile
import warnings
from urllib2 import HTTPError

def login(request):
    """ First step of process, redirects user to facebook, which redirects to authentication_callback. """

    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback'),
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args) + '&display=popup')

def authentication_callback(request):
    """ Second step of the login process.
    It reads in a code from Facebook, then redirects back to the home page. """
    code = request.GET.get('code')
    user = authenticate(token=code, request=request)

    if user.is_anonymous():
        #we have to set this user up
        url = reverse('facebook_setup')
        url += "?code=%s" % code

        resp = HttpResponseRedirect(url)

    else:
        auth_login(request, user)

        #figure out where to go after setup
        url = getattr(settings, "LOGIN_REDIRECT_URL", "/")

        resp = url(user)
    return resp

def make_wall_post(request, user_id, msg_string):

    the_user = FacebookProfile.objects.get(id = user_id)
    profile_id = the_user.user.username
    access_token = the_user.access_token

    path = profile_id + "/feed"

    post_args = {'message' : msg_string, 'access_token' : access_token}
    post_data = urllib.urlencode(post_args)

    query = "https://graph.facebook.com/" + path + "?" + urllib.urlencode({})

    try:
        file = urllib2.urlopen(query, post_data)
        raw = file.read()
    except HTTPError as e:
        if e.fp is not None:
            raise Exception, e.fp.read()
        else:
            raise Exception, e.fp.read()

    return HttpResponse(str(the_user.user.username) + " made post w msg '" + msg_string + "' w id " + raw)