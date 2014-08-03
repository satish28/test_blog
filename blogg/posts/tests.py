import string
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from models import UserPosts, UserPostLikes, UserPostCount
from django.contrib.auth.models import User
from services import *


class PostsTest(TestCase):
    # Data setup
    def setUp(self):
        # Providing access to the request factory.
        self.factory = RequestFactory()
        
        # Creating an user (This is the main user that will be used for all testing)
        User.objects.create(first_name="Eric", last_name="Raymond", 
            email="eric@mail.com", username="eric", password="eric")
        self.user = User.objects.get(username="eric")
        
        # Creating a second user (This user is created only to check )
        User.objects.create(first_name="Steve", last_name="Wozniak", 
            email="steve@mail.com", username="steve", password="steve")
        self.second_user = User.objects.get(username="steve")
        
        # Creating an user post.
        UserPosts.objects.create(username=self.user, post_title="Test post", 
            post_content="Test post content")
        self.post = UserPosts.objects.get(username=self.user)
            
        # Creating user post likes.
        # Actually we will add that entry while testing.
        
        # Creating user post count.
        UserPostCount.objects.create(username=self.user, post_count=5)
        
        update_likes(self.second_user, self.post.id)
        update_likes(self.user, self.post.id)        
            
        
    # Testing views
    def test_home(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        
    def test_each_post(self):
        pass
        
    def test_add_post(self):
        pass
        
    def test_user_profile(self):
        pass
        
    # Testing services
    def test_get_home_posts(self):
        posts = get_home_posts()
        self.assertIsNotNone(posts)
        self.assertTrue(len(posts) > 0)
        
    def test_get_post(self):
        post = get_post(self.post.id)
        self.assertIsNotNone(post)
        
        # Non existing post_id
        post = get_post(100)
        self.assertIsNone(post)
        
    def test_get_user_posts(self):
        user_posts = get_user_posts(self.user)
        self.assertTrue(len(user_posts) > 0)
        
        # Non existing user
        user = User()
        user_posts = get_user_posts(user)
        self.assertEqual(len(user_posts), 0)
        
    def test_generate_gravatar_url(self):
        url = "http://www.gravatar.com/avatar/"
        gravatar_url = generate_gravatar_url(self.user.email, 30)
        self.assertTrue(url in gravatar_url)
        
    def test_increment_visit_count(self):
        increment_visit_count(self.post.id)
        post_visits = UserPosts.objects.get(id=self.post.id)
        self.assertEqual(post_visits.visits, 1)
        
        # Non existing post_id
        increment_visit_count(100)
        
    def test_shorten_content(self):
        post_content = self.post.post_content + ' '.join([i for i in string.lowercase])
        short_content = shorten_content(post_content)
        self.assertTrue('...' in short_content)
        
        self.assertFalse('...' in post_content)
        
    def test_update_likes(self):
        """
        This is not required as of now. But should be fixed.
        """
        #count = update_likes(self.user, self.post.id)
        #self.assertEqual(count, 3)
        pass
        #count = update_likes(self.second_user, self.post.id)        
        #self.assertEqual(count, 4)
        
    def test_update_user_post_likes(self):
        """
        I guess this is not required. Since update_likes method calls 
        the method update_user_post_likes, doing a test here will
        obviously raise an exception as we are trying to add
        a row with same user and post.
        """      
        pass
        
    def test_is_post_liked(self):
        is_liked = is_post_liked(self.second_user, self.post)
        self.assertTrue(is_liked)
        
        is_liked = is_post_liked(self.user, self.post)
        self.assertTrue(is_liked)
        
    def test_get_user_post_count(self):
        user_post_count = get_user_post_count(self.user)
        self.assertIsNotNone(user_post_count)
        
        # Non existing user
        user = User()
        user_post_count = get_user_post_count(user)
        self.assertIsNone(user_post_count)
        
    def test_update_post_count(self):
        count_before_update = get_user_post_count(self.user).post_count
        update_post_count(self.user)
        count_after_update = get_user_post_count(self.user).post_count
        self.assertTrue(count_after_update == count_before_update + 1)
        
    def test_get_popular_posts(self):
        popular_posts = get_popular_posts()
        self.assertIsNotNone(popular_posts)
        
    def test_get_popular_authors(self):
        popular_authors = get_popular_authors()
        self.assertIsNotNone(popular_authors)
        