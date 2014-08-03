import hashlib
import urllib
from django.conf import settings
from models import UserPosts, UserPostLikes, UserPostCount

def get_home_posts():
    """
    Get posts to be displayed in the home page.
    """
    posts = UserPosts.objects.all().order_by('-created_timestamp')
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
    
def get_user_posts(user):
    """
    Get all posts by user user_id.
    """
    posts = UserPosts.objects.filter(username=user)
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
    if post:
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
    
def update_user_post_likes(user, post):
    """
    Update user likes in UserPostLikes table. Add an entry that user liked a post.
    A row in this table means the user liked corresponding post in the row.
    """
    user_likes = UserPostLikes(username=user, post=post)
    user_likes.save()
    
def is_post_liked(user, post):
    """
    Check if the post is already liked by the user and return True 
    if yes, else return False.
    """
    try:
        UserPostLikes.objects.get(username=user, post=post)
    except UserPostLikes.DoesNotExist:
        return False
    return True
    
def update_likes(user, post_id):
    """
    Update likes for post and return the updated like count.
    """
    post = get_post(post_id)
    likes = 0
    if post and not is_post_liked(user, post):
        # Updating user like also
        update_user_post_likes(user, post)
        post.likes += 1
        likes = post.likes
        post.save()
    return likes
    
def get_user_post_count(user):
    """
    Get the user post count if it exists else return None.
    """
    try:
        user_post_count = UserPostCount.objects.get(username=user)
    except UserPostCount.DoesNotExist:
        return None
    return user_post_count
    
def update_post_count(user):
    """
    Update post count of the user.
    """
    user_post_count = get_user_post_count(user)
    if user_post_count:
        user_post_count.post_count += 1
        user_post_count.save()
    else:
        user_post_count = UserPostCount(username=user, post_count=1)
        user_post_count.save()
        
def get_popular_posts():
    """
    Get popular_posts. (Based on no. of visits)
    """
    popular_post_count = settings.POPULAR_POST_COUNT
    popular_posts = UserPosts.objects.all().order_by('-visits')[:popular_post_count]
    return popular_posts

def get_popular_authors():
    """
    Get popular authors. (Based on no. of posts)
    """
    popular_author_count = settings.POPULAR_AUTHOR_COUNT
    popular_authors = UserPostCount.objects.all().order_by('-post_count')[:popular_author_count]
    return popular_authors
    
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
