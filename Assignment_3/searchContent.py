import webapp2
import jinja2
from userAuth import UserAuth
import os
from tweetsModel import TweetsModel
from google.appengine.api import search


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class SearchContent(webapp2.RequestHandler):
    def get(self):
        template_values = UserAuth(self.request.uri).userTemplateVals()
        if template_values['user'] == '' or template_values['user'] is None:
            template = JINJA_ENVIRONMENT.get_template('HTML/main.html')
            self.response.write(template.render(template_values))
        else:
            if template_values['username'] == '' or template_values['username'] is None:
                self.redirect('/register')
            else:
                template = JINJA_ENVIRONMENT.get_template('HTML/search-content.html')
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
                content = self.request.get('content')
                if len(content) > 0:
                    index = search.Index('tweets')
                    query_string = "tweets_content: "+content
                    query_options = search.QueryOptions(
                        limit=50
                    )
                    query = search.Query(query_string=query_string, options=query_options)
                    template_values['tweets'] = index.search(query)
                else:
                    template_values['err_msg'] = 'Search Content is required.'
                print(template_values)
                template = JINJA_ENVIRONMENT.get_template('HTML/search-content.html')
                self.response.write(template.render(template_values))