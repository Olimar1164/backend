from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.core import mail
from contactos.models import Contacto
from users.models import CustomUser


class ContactoModelTest(TestCase):
    def setUp(self):
        self.contacto = Contacto.objects.create(
            nombre='Test User',
            email='test@example.com',
            mensaje='This is a test message.'
        )

    def test_contacto_creation(self):
        self.assertEqual(self.contacto.nombre, 'Test User')
        self.assertEqual(self.contacto.email, 'test@example.com')
        self.assertEqual(self.contacto.mensaje, 'This is a test message.')


class ContactoViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_contacto_view_authenticated(self):
        response = self.client.get(reverse('contacto-list'))
        self.assertEqual(response.status_code, 200)

    def test_contacto_view_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(reverse('contacto-list'))
        self.assertEqual(response.status_code, 401)