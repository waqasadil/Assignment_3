import webapp2
import jinja2
from userAuth import UserAuth
import os
from google.appengine.ext import ndb

from userModel import UserModel
from followInfoModel import FollowInfoModel
from tweetsModel import TweetsModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class SearchUser(webapp2.RequestHandler):
    def get(self):
        template_values = UserAuth(self.request.uri).userTemplateVals()
        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('HTML/main.html')
            self.response.write(template.render(template_values))
        else:
            if template_values['username'] == '' or template_values['username'] is None:
                self.redirect('/register')
            else:
                template = JINJA_ENVIRONMENT.get_template('HTML/search-user.html')
                self.response.write(template.render(template_values))

    def post(self):
        template_values = UserAuth(self.request.uri).userTemplateVals()

        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('HTML/main.html')
            self.response.write(template.render(template_values))
        else:
            action = self.request.get('button')
            if action.lower() == 'search':
                err_msg = ''
                user_name = self.request.get('userName')
                if len(user_name) > 0:
                    template_values['search'] = user_name
                    user_key = ndb.Key(UserModel, user_name)
                    get_user = user_key.get()
                    follow_info_key = ndb.Key(FollowInfoModel, user_name)
                    get_follow_info = follow_info_key.get()
                    tweet_model_query = TweetsModel.query(TweetsModel.user_name == user_name).order(-TweetsModel.updated_date)
                    page_size=50
                    template_values['tweets'] = tweet_model_query.fetch(page_size)
                    if get_follow_info == '' or get_follow_info is None:
                        template_values['following'] = False
                    else:
                        if template_values['username'] in get_follow_info.followed_by:
                            template_values['following'] = True
                        else:
                            template_values['following'] = False
                    if get_user == '' or get_user is None:
                        err_msg = 'User Not Found.'
                    else:
                        template_values['userInfo'] = get_user
                else:
                    err_msg = 'Username is required.'
                template_values['err_msg'] = err_msg
                template = JINJA_ENVIRONMENT.get_template('HTML/search-user.html')
                self.response.write(template.render(template_values))
            elif action.lower() == 'follow':
                current_user = template_values['username']
                search_user = self.request.get('userName')
                follow_to_info_key = ndb.Key(FollowInfoModel, current_user)
                get_follow_to_info = follow_to_info_key.get()
                follow_to_model = FollowInfoModel()
                follow_to_model.key = follow_to_info_key
                if get_follow_to_info == '' or get_follow_to_info is None:
                    follow_to_model.followed_to = [search_user]
                    follow_to_model.put()
                else:
                    get_follow_to_info.followed_to.append(search_user) if search_user not in get_follow_to_info.followed_to else get_follow_to_info.followed_to
                    get_follow_to_info.put()

                follow_by_info_key = ndb.Key(FollowInfoModel, search_user)
                get_follow_by_info = follow_by_info_key.get()
                follow_by_model = FollowInfoModel()
                follow_by_model.key = follow_by_info_key
                if get_follow_by_info == '' or get_follow_by_info is None:
                    follow_by_model.followed_by = [current_user]
                    follow_by_model.put()
                else:
                    get_follow_by_info.followed_by.append(current_user) if current_user not in get_follow_by_info.followed_by else get_follow_by_info.followed_by
                    get_follow_by_info.put()
                self.redirect('/home')
            elif action.lower() == 'unfollow':
                current_user = template_values['username']
                search_user = self.request.get('userName')
                follow_to_info_key = ndb.Key(FollowInfoModel, current_user)
                get_followed_to = follow_to_info_key.get()
                get_followed_to.followed_to.remove(search_user)
                get_followed_to.put()
                follow_by_info_key = ndb.Key(FollowInfoModel, search_user)
                get_followed_by = follow_by_info_key.get()
                get_followed_by.followed_by.remove(current_user)
                get_followed_by.put()
                self.redirect('/home')
