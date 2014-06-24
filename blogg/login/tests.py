from django.test import TestCase
from django.core.urlresolvers import reverse


class LoginViewsTestCase(TestCase):
    def test_user_login(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        
    def test_user_register(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)
        
    def test_user_logout(self):
        resp = self.client.get(reverse('logout'))
        # status code: 302 for redirection
        self.assertEqual(resp.status_code, 302)