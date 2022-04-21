from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

# Create your tests here.
class PostTest(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
                username='admin',
                email='admin@email.com',
                password='123')

        self.user = get_user_model().objects.create_user(
                username='user',
                email='user@email.com',
                password='123')
        
    
    def test_create_post_for_admin(self):
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('post_view'), {"title": "testTitle", "body": "testBody"})
        self.assertEqual(response.status_code, 201)

    def test_create_post_for_users(self):
        self.client.login(username='user', password='123')
        response = self.client.post(reverse('post_view'), {"title": "testTitle", "body": "testBody"})
        self.assertEqual(response.status_code, 403)

    def test_create_post_for_anounymouse_users(self):
        self.client.logout()
        response = self.client.post(reverse('post_view'), {"title": "testTitle", "body": "testBody"})
        self.assertEqual(response.status_code, 401)

    def test_post_list_for_logged_in_user(self):
        self.client.login(username='user', password='123')
        response = self.client.get(reverse('post_view'))
        self.assertEqual(response.status_code, 200)
    
    def test_post_list_for_anounymouse_users(self):
        self.client.logout()
        response = self.client.get(reverse('post_view'))
        self.assertEqual(response.status_code, 200)


class RatingTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
                username='user',
                email='user@email.com',
                password='123')
                
        Post.objects.create(title="title", body="dsfds")

    def test_voting_for_logged_in_users(self):
        self.client.login(username='user', password='123')
        response = self.client.post(reverse('rating_view'), {"post": "1", "score": "3"})
        self.assertEqual(response.status_code, 201)
 
    def test_voting_for_anounymouse_users(self):
        self.client.logout()
        response = self.client.post(reverse('rating_view'), {"post": "1", "score": "3"})
        self.assertEqual(response.status_code, 401)

    def test_invalid_score(self):
        self.client.login(username='user', password='123')
        response = self.client.post(reverse('rating_view'), {"post": "1", "score": "6"})
        self.assertEqual(response.status_code, 400)