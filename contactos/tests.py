from django.test import TestCase
from contactos.models import Contacto

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