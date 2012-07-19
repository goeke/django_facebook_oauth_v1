import json, urllib

from django.db import models
from django.contrib.auth.models import User

class FacebookProfile(models.Model):
    user = models.OneToOneField(User)
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(max_length=150)

    def get_facebook_profile(self):
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % self.access_token)
        return json.load(fb_profile)
        
    def get_facebook_friends(self):
        fb_friends = urllib.urlopen('https://graph.facebook.com/me/friends?access_token=%s' % self.access_token)
        return json.load(fb_friends)

    def __unicode__(self):
        print(dir(self.user))
        return str(self.user.username)