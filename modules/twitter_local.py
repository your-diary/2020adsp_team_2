#!/usr/bin/env python3

import os
import re
import time

import twitter

import modules.json_local as json_local

#-------------------------------------#

### Tweet Class ###

class Tweet:

    def __init__(self, tweet: twitter.models.Status) -> None:

        self.tweet: twitter.models.Status = tweet

        self.tweet_id:         int = self.tweet.id
        self.user_screen_name: str = self.tweet.user.screen_name
        self.user_id:          str = self.tweet.user.id
        self.user_name:        str = self.tweet.user.name
        self.content:          str = self.tweet.text
        self.timestamp_unix:   int = time.mktime(time.strptime(self.tweet.created_at, '%a %b %d %H:%M:%S %z %Y')) + 9 * 3600
        self.timestamp:        str = time.strftime('%Y/%m/%d(%a)%H:%M:%S%z', time.localtime(self.timestamp_unix))
        self.like_count:       int = self.tweet.favorite_count
        self.retweet_count:    int = self.tweet.retweet_count

    def __str__(self) -> str:
        ret: str = '---------- Tweet ----------\n'
        l: int = len(ret) - 1
        for key in self.__dict__:
            if (key == 'tweet' or key == 'timestamp_unix' or key == 'content'):
                continue
            ret += f'{key:17s}: {self.__dict__[key]}\n'
        ret += '\n' + self.content + '\n'
        for i in range(l):
            ret += '-'
        return ret

#-------------------------------------#

### TwitterUser Class ###

class TwitterUser:

    def __init__(self, user: twitter.models.User) -> None:

        self.user: twitter.models.User = user

        self.id:          int = self.user.id
        self.screen_name: str = self.user.screen_name
        self.name:        str = self.user.name
        
        self.is_protected: bool = self.user.protected

        self.profile_text: str = self.user.description
        self.location:     str = self.user.location
        self.homepage_url: str = self.user.url

        self.profile_image_url: str = self.user.profile_image_url_https.replace('_normal', '')
        self.header_image_url:  str = self.user.profile_banner_url

        self.num_follow:   int = self.user.friends_count
        self.num_follower: int = self.user.followers_count

        self.num_tweet: int = self.user.statuses_count
        self.num_like:  int = self.user.favourites_count

        self.creation_date_unix: int = time.mktime(time.strptime(self.user.created_at, '%a %b %d %H:%M:%S %z %Y')) + 9 * 3600
        self.creation_date:      str = time.strftime('%Y/%m/%d(%a)%H:%M:%S%z', time.localtime(self.creation_date_unix))

        self.last_tweet: twitter.models.Status = self.user.status

    def __str__(self) -> str:
        ret: str = f'---------- {self.name} (@{self.screen_name}) ----------\n'
        l: int = len(ret) - 1
        for key in self.__dict__:
            if (key == 'user' or key == 'last_tweet'):
                continue
            ret += f'{key:19s}: {self.__dict__[key]}\n'
        for i in range(l):
            ret += '-'
        return ret

#-------------------------------------#

### Twitter Class ###

class Twitter:

    def __init__(self, twitter_credentials_file: str, timeout_sec: int = 30, num_trial: int = 3, is_verbose_mode: bool = False):

        twitter_credentials: dict = json_local.json_loadf(twitter_credentials_file, should_interpret_comment = True)

        print('Twitter: Logging in...')
        self.twitter_client: object = twitter.Api(
                                                   consumer_key        = twitter_credentials['api_key'],
                                                   consumer_secret     = twitter_credentials['api_secret_key'],
                                                   access_token_key    = twitter_credentials['access_token'],
                                                   access_token_secret = twitter_credentials['access_token_secret'],
                                                   timeout             = timeout_sec
                                                 )
        print('Twitter: Logged in.')

        self.num_trial: int = num_trial
        self.is_verbose_mode: bool = is_verbose_mode

        self.ret: object = None
        self.tmp: object = None

    def __debug_print(self, *args, **kwargs) -> None:
        if (self.is_verbose_mode):
            print(*args, **kwargs)

    def __exec(self, statement: str) -> object:
        for i in range(self.num_trial):
            try:
                self.__debug_print(f'Twitter.__exec(): Executing [ {statement} ]... ', end = '', flush = True)
                time.sleep(3)
                exec(statement)
                self.__debug_print(f'Done.')
                break
            except Exception as e:
                self.__debug_print('Failed.')
                if (i == self.num_trial - 1):
                    raise e
                else:
                    self.__debug_print(f'Twitter.__exec(): Retrying...')
        return self.ret

    def post_tweet(self, tweet_content: str, media_file: str = '') -> None:
        if (media_file == ''):
            self.__exec(f'self.twitter_client.PostUpdate(status = "{tweet_content}")')
        else:
            self.__exec(f'self.twitter_client.PostUpdate(status = "{tweet_content}", media = "{media_file}")')

    def upload_video(self, tweeted_content: str, video_file: str, wait_media_processing_sec: float = 10) -> None:
        
        video_id: int = None

        for i in range(num_trial):
            try:
                if (video_id is None):
                    video_id: int = self.twitter_client.UploadMediaChunked(media = video_file, media_category = 'tweet_video')

                time.sleep(wait_media_processing_sec)

                self.twitter_client.PostUpdate(status = tweeted_content, media = video_id)

                break

            except Exception as e:
                if (i == self.num_trial - 1):
                    raise e
                else:
                    pass

    def upload_image(self, image_file: str) -> int:
        image_id: int = self.twitter_client.UploadMediaSimple(media = image_file) #e.g. 1305905212285042689
        return image_id

    def get_likes(self, screen_name: str = None, num_retrieve: int = 200) -> list:
        if (screen_name is None):
            likes: list = self.__exec(f'self.ret = self.twitter_client.GetFavorites(count = {num_retrieve})')
        else:
            likes: list = self.__exec(f'self.ret = self.twitter_client.GetFavorites(screen_name = "{screen_name}", count = {num_retrieve})')
        return likes

    def remove_like(self, tweet: twitter.models.Status) -> None:
        self.tmp = tweet
        self.__exec('self.twitter_client.DestroyFavorite(self.tmp)')

    def create_like(self, tweet: twitter.models.Status) -> None:
        self.tmp = tweet
        self.__exec('self.twitter_client.CreateFavorite(self.tmp)')

    def create_retweet(self, tweet: twitter.models.Status) -> None:
        self.tmp = tweet.id
        self.__exec('self.twitter_client.PostRetweet(self.tmp)')

    def get_user_information(self, screen_name: str = None, user_id: int = None) -> twitter.models.User:
        if (((user_id is None) and (screen_name is not None)) or ((user_id is not None) and (screen_name is None))):
            self.__exec(f'self.ret = self.twitter_client.GetUser(user_id = {user_id}, screen_name = "{screen_name}")')
            return self.ret
        else:
            raise Exception('Twitter.get_user_information(): Only one of `user_id` or `screen_name` shall be specified.')

    def get_user_tweets(self, screen_name: str, num_retrieve: int = 200, since_id: str = None, should_include_rt: bool = True) -> list:
        command: str = f'self.ret = self.twitter_client.GetUserTimeline(screen_name = "{screen_name}", count = {num_retrieve}, include_rts = {should_include_rt}'
        if (since_id is not None):
            command += f', since_id = "{since_id}"'
        command += ')'
        return self.__exec(command)

    #Input:
    #  1. `since_id` a tweet id. Tweets newer than the tweet will be retrieved.
    #  2. `since` and `until` are of the form "YYYY-MM-DD". `since` is inclusive while `until` is exclusive.
    #  3. `lang` is an ISO 639-1 code such as "ja". See |https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes| for the list.
    #Output:
    #  1. `search_result[0]` is the latest tweet and `search_result[-1]` is the oldest tweet.
    def search(self, search_keyword: str, num_retrieve: int = 100, since_id: int = None, since: str = None, until: str = None, lang: str = None, result_type: str = "recent") -> list:
        command: str = f'self.ret = self.twitter_client.GetSearch(term = "{search_keyword}", count = {num_retrieve}, result_type = "{result_type}", since_id = {since_id}'
        if (since is not None):
            assert (re.search(r'^\d\d\d\d-\d\d-\d\d$', since) is not None)
            command += f', since = "{since}"'
        if (until is not None):
            assert (re.search(r'^\d\d\d\d-\d\d-\d\d$', until) is not None)
            command += f', until = "{until}"'
        if (lang is not None):
            command += f', lang = "{lang}"'
        command += ')'
        search_result: list = self.__exec(command)
        return search_result

    def update_header_image(self, image_file: str) -> None:
        self.__exec(f'self.twitter_client.UpdateBanner("{image_file}")')

    def update_profile_image(self, image_file: str) -> None:
        self.__exec(f'self.twitter_client.UpdateImage("{image_file}")')

    def update_profile(self, username: str = None, description: str = None, url: str = None, location: str = None) -> None:
        command: str = f'self.twitter_client.UpdateProfile('
        if (username is not None):
            command += f'name = "{username}", '
        if (description is not None):
            command += f'description = "{description}", '
        if (url is not None):
            command += f'profileURL = "{url}", '
        if (location is not None):
            command += f'location = "{location}", '
        command += ')'
        self.__exec(command)

#-------------------------------------#

