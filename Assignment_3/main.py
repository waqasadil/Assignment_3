import webapp2
import jinja2
import os
from userAuth import UserAuth
from home import Home, PhotoUploadHandler
from register import Register
from profile import Profile
from EditUserProfile import EditUserProfile
from Edittweet import Edittweet
from searchUser import SearchUser
from searchContent import SearchContent

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = UserAuth(self.request.uri).userTemplateVals()
        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('HTML/main.html')
            self.response.write(template.render(template_values))
        else:
            if template_values['username'] == '' or template_values['username'] is None:
                self.redirect('/register')
            else:
                self.redirect('/home')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/home', Home),
    ('/register', Register),
    ('/profile', Profile),
    ('/profile-edit', EditUserProfile),
    ('/tweet-edit', Edittweet),
    ('/search-user', SearchUser),
    ('/search-content', SearchContent),
    ('/upload', PhotoUploadHandler),
], debug=True)