import webapp2
import jinja2
from userAuth import UserAuth
import os
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url

from tweetsModel import TweetsModel
from followInfoModel import FollowInfoModel
from google.appengine.api import search

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Home(webapp2.RequestHandler):
    def get(self):
        template_values = UserAuth(self.request.uri).userTemplateVals()
        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('HTML/main.html')
            self.response.write(template.render(template_values))
        else:
            if template_values['username'] == '' or template_values['username'] is None:
                self.redirect('/register')
            else:
                template_values['tweets'] = self.getTweets(template_values['username'])
                template_values['upload_url'] = blobstore.create_upload_url('/upload')
                template = JINJA_ENVIRONMENT.get_template('HTML/home.html')
                self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')
        if (action.lower()) == 'delete':
             tweet_id = int(self.request.get('tweet_id'))
             ndb.Key(TweetsModel, tweet_id).delete()
             self.redirect('/home')

    def getTweets(self, username):
        user_list = [username]
        PAGE_SIZE = 50
        follow_info_key = ndb.Key(FollowInfoModel, username)
        get_follow_info = follow_info_key.get()
        if get_follow_info and get_follow_info.followed_to:
            user_list += user_list+get_follow_info.followed_to
        tweet_query = TweetsModel.query(TweetsModel.user_name.IN(user_list)).order(-TweetsModel.updated_date)
        tweet_fetch = tweet_query.fetch(PAGE_SIZE)
        return tweet_fetch


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        template_values = UserAuth(self.request.uri).userTemplateVals()
        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('HTML/main.html')
            self.response.write(template.render(template_values))
        else:
            action = self.request.get('button')
            tweets_content = self.request.get('tweet_content')

            if action.lower() == 'tweet':
                tweets_content = self.request.get('tweet_content')
                if len(tweets_content) > 280:
                    template_values['tweets_content'] = tweets_content
                    template_values['tweets'] = self.getTweets(template_values['username'])
                    template_values['err_msg'] = 'Content can not be more than 280 characters.'
                    template = JINJA_ENVIRONMENT.get_template('HTML/home.html')
                    self.response.write(template.render(template_values))
                else:
                    tweets_model = TweetsModel()
                    tweets_model.user_name = template_values['username']
                    tweets_model.tweet_content = tweets_content
                    img_url = ''
                    if len(self.get_uploads()) > 0:
                        upload = self.get_uploads()[0]
                        blobinfo = blobstore.BlobInfo(upload.key())
                        filename = blobinfo.filename
                        tweets_model.tweet_image = upload.key()
                        img_url = get_serving_url(upload.key())
                        tweets_model.tweet_image_url = get_serving_url(upload.key())
                    tweets_model.put()
                    document = search.Document(
                        fields = [
                            search.TextField('tweets_content', tweets_content),
                            search.TextField('username', template_values['username']),
                            search.TextField('image_url', img_url)
                        ]
                    )
                    index = search.Index('tweets')
                    index.put(document)
                    self.redirect('/home')
