import json
import base64

from django.urls import reverse

from rest_framework.test import APITestCase


class EntrepreneurAPITestCase(APITestCase):

    def test_onboarding_and_login(self):
        email = "john.doe@mail.com"
        password = "P@ssword1234"

        # register
        response = self.client.post(reverse('api:entrepreneurs-create'), data={
            'email': email, 'first_name': 'john', 'last_name': 'doe', 'password': password,
        })

        self.assertEqual(201, response.status_code)

        # login, retrieve the token
        credentials = base64.b64encode(f'{email}:{password}'.encode('utf-8'))
        self.client.credentials(HTTP_AUTHORIZATION='Basic {}'.format(credentials.decode('utf-8')))

        response = self.client.post(reverse('api:knox_login'))
        self.assertEquals(200, response.status_code)

        self.assertIn('token', response.data)
        self.assertIn('expiry', response.data)
        self.assertIn('user', response.data)

        token = response.data['token']

        # try an authenticated endpoint
        self.client.credentials()  # clear all credentials
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.get(reverse('api:entrepreneurs-list'))
        self.assertEqual(200, response.status_code)

        self.assertEqual(1, len(response.data))
        item = response.data[0]
        self.assertIn('email', item)
        self.assertEqual(email, item['email'])
        self.assertIn('first_name', item)
        self.assertEqual('John', item['first_name'])
        self.assertIn('last_name', item)
        self.assertEqual('Doe', item['last_name'])

        # logout
        response = self.client.post(reverse('api:knox_logout'))
        self.assertEquals(204, response.status_code)
