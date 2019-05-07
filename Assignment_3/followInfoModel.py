from google.appengine.ext import ndb


class FollowInfoModel(ndb.Model):
    followed_to = ndb.StringProperty(repeated=True)
    followed_by = ndb.StringProperty(repeated=True)