from django.test import TestCase
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


# Create your tests here.

class UserTest(TestCase):

    def test_user(self):
        self.assertFalse(User.objects.exists())
        USERNAME = 'lockepw'
        EMAIL = 'locke@hegemony.gov'
        PASSWORD = 'FREJKHRKJFH*^&987324'

        client = APIClient()
        data = {
            'username': USERNAME,
            'email': EMAIL,
            'password': PASSWORD,
        }
        response = client.post(reverse('user-list'),
                               data,
                               format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        print User.objects.first().password

        print 'testing login 1'

        #def test_logout(self):
        #c = self.client
        response = client.get(reverse('api-logout'))
        self.assertEqual(response.status_code, 200)

        #def test_login(self):
        #c = self.client
        response = client.post(
            reverse('api-login'),
            data={'username': USERNAME,
                  'password': PASSWORD})
        print response.content
        #self.assertEqual(response.status_code, 200)


        print 'testing login 2'
        # test logging in
        response = client.post(
            reverse('api-login'),
            {
                'username': USERNAME,
                #'email': EMAIL,
                'password': PASSWORD
            },
            format='json')
        print 'content'
        print response.content
        print response.status_code