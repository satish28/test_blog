import hashlib
import urllib
from models import UserPosts, UserLikes

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
    
def increment_visit_count(post_id):
    """
    Increment the visit count of the post. We can directly use the post
    object for incrementing. But it will show visit count at first visit 
    itself. We want the visits to be incremented only after the post is
    read. So the visit will be reflected the next time the post is opened.
    """
    post = get_post(post_id)
    post.visits += 1
    post.save()
    
def shorten_content(post_content):
    """
    Shorten content to be displayed in home page.
    """
    no_of_words = 20
    words = post_content.split(' ')
    reduced_words = words[:no_of_words]
    content = ' '.join(reduced_words)
    if len(words) > no_of_words:
        content += '...'
    return content

def hard_delete_post(post_id):
    """
    Delete a Post.
    """
    UserPosts.objects.filter(id=post_id).delete() 	
    
def update_user_like(user, post):
    """
    Update user like in UserLikes table.
    """
    user_like = UserLikes(username=user, post=post)
    user_like.save()
    
def is_post_liked(user, post):
    """
    Check if the post is already liked by the user and return True 
    if yes, else return False.
    """
    try:
        UserLikes.objects.get(username=user, post=post)
    except UserLikes.DoesNotExist:
        return False
    return True
    
def update_likes(user, post_id):
    """
    Update likes for post and return the updated like count.
    """
    post = get_post(post_id)
    if post and not is_post_liked(user, post):
        # Updating user like also
        update_user_like(user, post)
        post.likes += 1
        likes = post.likes
        post.save()
    return likes
    
class PostWithImage():
    """
    Object with post and email. This is primarily done to get email hash.
    This object will be used in home page.
    """
    def __init__(self, post, email, size):
        self.post = post
        self.email = email
        self.size = size
        self.gravatar_url = generate_gravatar_url(self.email, self.size)
        self.post.post_content = shorten_content(post.post_content)
        
    def __str__(self):
        return str(self.post) + self.gravatar_url + self.size
