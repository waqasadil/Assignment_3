from google.appengine.ext import ndb


class TweetsModel(ndb.Model):
    tweet_content = ndb.StringProperty()
    tweet_content_lower = ndb.ComputedProperty(lambda self: self.tweet_content.lower())
    tweet_image = ndb.BlobKeyProperty()
    tweet_image_url = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    updated_date = ndb.DateTimeProperty(auto_now_add=True)
    user_name = ndb.StringProperty()
