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