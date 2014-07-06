import hashlib
import urllib
from models import UserPosts

def get_home_posts():
    """
    Get posts to be displayed in the home page.
    """
    posts = UserPosts.objects.all()
    return posts

def get_post(post_id):
    """
    Get post object with id post_id if it exists, else return None.
    """
    try:
        post = UserPosts.objects.get(id=post_id)
    except UserPosts.DoesNotExist:
        post = None
    return post
    
def get_user_posts(user_id):
    """
    Get posts by user user_id.
    """
    posts = UserPosts.objects.filter(username_id=user_id)
    return posts
    
def generate_gravatar_url(email, size):
    """
    Generate gravatar url for getting user image.
    """
    default_image_url = ''
    hash_obj = hashlib.md5(email)
    email_hash = hash_obj.hexdigest()
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default_image_url, 's':str(size)})
    return gravatar_url
    
class PostWithImage():
    """
    Object with post and email. This is primarily done to get email hash.
    """
    def __init__(self, post, email, size):
        self.post = post
        self.email = email
        self.size = size
        self.gravatar_url = generate_gravatar_url(self.email, self.size)
        
    def __str__(self):
        return str(self.post) + self.gravatar_url + self.size
        