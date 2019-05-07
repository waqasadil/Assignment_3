import webapp2
import jinja2
from userAuth import UserAuth
import os
from userModel import UserModel
from google.appengine.ext import ndb
from followInfoModel import FollowInfoModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Profile(webapp2.RequestHandler):
    def get(self):
        template_values = UserAuth(self.request.uri).userTemplateVals()
        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('HTML/main.html')
            self.response.write(template.render(template_values))
        else:
            if template_values['username'] == '' or template_values['username'] is None:
                self.redirect('/register')
            else:
                user_model = UserModel()
                user_key = ndb.Key(UserModel, template_values['username'])
                user_model.key = user_key
                get_user = user_key.get()
                template_values['userInfo'] = get_user
                follow_info_model = FollowInfoModel()
                follow_key = ndb.Key(FollowInfoModel, template_values['username'])
                get_follow_info = follow_key.get()
                template_values['follow_info'] = get_follow_info
                print(get_follow_info)
                template = JINJA_ENVIRONMENT.get_template('HTML/profile.html')
                self.response.write(template.render(template_values))
