from django.test import TestCase
from django.core.urlresolvers import reverse


class PostsTest(TestCase):
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
        pass
        
    def test_get_post(self):
        pass
        
    def test_get_user_profile(self):
        pass
        
    def test_generate_gravatar_url(self):
        pass
        
    def test_increment_visit_count(self):
        pass
        
    def test_shorten_content(self):
        pass
        
    def update_likes(self):
        pass