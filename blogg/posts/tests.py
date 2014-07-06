from django.test import TestCase
from django.core.urlresolvers import reverse


class PostsTest(TestCase):
    def test_home(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        
    def test_each_post(self):
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