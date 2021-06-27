from django.urls import reverse, resolve
from .views import home, register, Login, Logout, Subjects, result
from django.test import SimpleTestCase, TestCase, Client
from django.contrib.auth.models import User
from .models import Subject, Quiz_data, Quiz
import json

class TestUrls(SimpleTestCase):
    def test_home_urls_resolve(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEqual(resolve(url).func, home)


    def test_register_urls_resolve(self):
        url = reverse('register')
        print(resolve(url))
        self.assertEqual(resolve(url).func, register)

    def test_login_urls_resolve(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEqual(resolve(url).func, Login)

    def test_logout_urls_resolve(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEqual(resolve(url).func, Logout)

    def test_quiz_urls_resolve(self):
        url = reverse('quiz')
        print(resolve(url))
        self.assertEqual(resolve(url).func, Subjects)


    def test_result_urls_resolve(self):
        url = reverse('result')
        print(resolve(url))
        self.assertEqual(resolve(url).func, result)



class Test_views(TestCase):

    def setUp(self):
        self.client = Client()
        self.home = reverse('home')
        self.login = reverse('login')
        self.register = reverse('register')


    def test_home_get(self):

        response = self.client.get(self.home)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_register_get(self):

        response = self.client.get(self.register)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_post_sucess(self):
        response = self.client.post(self.register, {
            'username': 'user1',
            'email': 'user@gmail.com',
            'password': 'pas12345'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(User.objects.count(), 1)




    def test_login_get(self):

        response = self.client.get(self.login)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post(self):
        response = self.client.post(self.login, {'username': 'user3', 'password': 'pas12345'})
        self.assertEquals(response.status_code, 200)
