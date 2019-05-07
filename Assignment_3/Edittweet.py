import webapp2
import jinja2
from userAuth import UserAuth
import os
from userModel import UserModel
from google.appengine.ext import ndb
from datetime import datetime
from tweetsModel import TweetsModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Edittweet(webapp2.RequestHandler):
    def get(self):
        template_values = UserAuth(self.request.uri).userTemplateVals()
        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('HTML/main.html')
            self.response.write(template.render(template_values))
        else:
            if template_values['username'] == '' or template_values['username'] is None:
                self.redirect('/register')
            else:
                tweet_id = int(self.request.get('id'))
                tweet_model = ndb.Key(TweetsModel, tweet_id)
                template_values['tweetData'] = tweet_model.get()
                template = JINJA_ENVIRONMENT.get_template('HTML/tweet-edit.html')
                self.response.write(template.render(template_values))

    def post(self):
        template_values = UserAuth(self.request.uri).userTemplateVals()

        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('HTML/main.html')
            self.response.write(template.render(template_values))
        else:
            action = self.request.get('button')
            print(action)
            if action.lower() == 'submit':
                tweets_content = self.request.get('tweet_content')
                if len(tweets_content) > 280:
                    err_msg = 'Content can not be more than 280 characters.'
                else:
                    tweet_id = int(self.request.get('id'))
                    tweet_key = ndb.Key(TweetsModel, tweet_id)
                    get_tweet = tweet_key.get()
                    get_tweet.tweet_content = tweets_content
                    get_tweet.updated_date = datetime.now()
                    get_tweet.put()
                self.redirect('/home')

