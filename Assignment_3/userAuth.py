import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from userModel import UserModel


class UserAuth(webapp2.RequestHandler):
    def __init__(self, requesturi):
        self.requesturi = requesturi

    def userTemplateVals(self):
        url = ''
        url_string = ''
        username = ''
        user = users.get_current_user()
        if user:
            url = users.create_logout_url('/')
            url_string = 'Logout'
            userEmail = "%s" % (user)
            get_user = UserModel.query(UserModel.email==userEmail).fetch()
            if get_user and len(get_user)>0:
                userInfo = get_user[0]
                if userInfo.user_name:
                    username = userInfo.user_name
                else:
                    username = ''
            else:
                username = ''
        else:
            url = users.create_login_url(self.requesturi)
            url_string = 'Login'

        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'username': username
        }
        return template_values
