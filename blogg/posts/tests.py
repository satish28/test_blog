from django.test import TestCase
from django.core.urlresolvers import reverse


class PostsTest(TestCase):
    def test_home(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        
    def test_each_post(self):
        pass