from google.appengine.ext import ndb


class UserModel(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    user_name = ndb.StringProperty()
    user_profile = ndb.StringProperty()
    followed_by_count = ndb.IntegerProperty(default=0)
    followed_to_count = ndb.IntegerProperty(default=0)
