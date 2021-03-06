#!/usr/bin/env python
#
#   Copyright 2014 Frite M.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import tweepy as tweepy
import alertsClass as alerts


# Add TwitterError exception handling


class TwitterService:
    '''
    Base class handling all twitter requests based on Tweepy api.
    In most of the cases it returns *JSON-ENCODED STRINGS*
    '''
    api = None;
    oTextColor = alerts.textAlert()

    def __init__(self, cKey, cSecret, atKey, atSecret, name):
        auth = tweepy.OAuthHandler(cKey, cSecret)
        auth.set_access_token(atKey, atSecret)
        self.api = tweepy.API(auth)
        self.oTextColor.okblue("\t[NOTICE]\tRunning self-test on verification")
        if (self.verify_credentials() == name):
            self.oTextColor.okgreen("\t[SUCCESS]\t Self-verification succeeded")
        else:
            self.oTextColor.warning("\t[WARNING*]\t Self-verification failed")
            raise SystemExit

    def verify_credentials(self):
        #  Authorization test
        try:
            twitterCredentials = self.api.me().name
            return twitterCredentials
        except tweepy.TweepError as e:
            self.oTextColor.warning("Something happened. " + e.reason)
            raise SystemExit

    def get_user(self, name=None, UID=None):
        #  Returns user object
        if UID is None:
            self.oTextColor.okblue("\t[NOTICE]\t Querying for user %s" % name)
            jsonUserData = self.execute(self.api.get_user, name)
        elif name is None:
            self.oTextColor.okblue("\t[NOTICE]\t Querying for user %s" % UID)
            jsonUserData = self.execute(self.api.get_user(user_id=UID))
        return jsonUserData

    def get_friends(self, name=None, UID=None):
        #  Returns a list of user IDs that a certain user follows
        if UID is None:
            self.oTextColor.okblue("\t[NOTICE]\t Querying for %s's friends" % name)
            jsonFriendsList = self.api.friends_ids(screen_name=name)
        elif name is None:
            self.oTextColor.okblue("\t[NOTICE]\t Querying for %s's friends" % UID)
            jsonFriendsList = self.api.friends_ids(user_id=UID)
        return jsonFriendsList

    def get_followers(self, userObject):
        #  Returns a list of user IDs that follow a certain user
        self.oTextColor.okblue("\t[NOTICE]\t Querying for %s's followers" % userObject.screen_name)
        jsonFollowersList = []
        count = -1
        while ((count < 10) and (userObject.followers_count > jsonFollowersList.__len__())):
            try:
                jsonFollowersList += self.api.followers_ids(screen_name=userObject.screen_name)
                count += 1
            except:
                self.oTextColor.warning("\t[*WARNING*]\t LIMIT REACHED")
                return jsonFollowersList
        return jsonFollowersList

    def get_tweets(self, name=None, UID=None, tweets=200, rts=True, entities=True):
        #  Returns a list of tweet objects '''
        n = 0
        page_list = []
        for page in tweepy.Cursor(self.api.user_timeline, screen_name=name, count=200, include_rts=rts).pages(16):
            page_list.append(page)
            n = n + 1
        statuses = []
        for page in page_list:
            for status in page:
                statuses.append(status)
        return statuses

    def execute(self, function, parameter):
        try:
            print parameter
            return function(parameter)
        except tweepy.TweepError as e:
            self.oTextColor.warning(
                "\t[WARNING]\tSomething happened. Sleeping for a minute. %s" % (str(e.message[0]['message'])))
            raise SystemExit
