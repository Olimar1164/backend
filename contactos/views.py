from django.http import JsonResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from contactos.models import Contacto
from users.models import CustomUser
from contactos.serializers import ContactoSerializer, UserSerializer
import logging

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': request.META.get('CSRF_COOKIE')})

class CustomTokenObtainPairView(TokenObtainPairView):
    pass

class CustomTokenRefreshView(TokenRefreshView):
    pass

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

import requests
from rest_framework import serializers


class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all().select_related()
    serializer_class = ContactoSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        captcha_token = self.request.data.get('captchaToken')
        secret_key = settings.HCAPTCHA_SECRET_KEY

        # Verificar el token de hCaptcha
        response = requests.post(
            settings.HCAPTCHA_VERIFY_URL,
            data={
                'secret': secret_key,
                'response': captcha_token
            }
        )
        result = response.json()
        if not result.get('success'):
            raise serializers.ValidationError('hCaptcha verification failed')

        contacto = serializer.save()
        subject = f'Nuevo mensaje de {contacto.nombre}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [settings.CONTACT_EMAIL]
        
        # Renderizar la plantilla HTML
        html_content = render_to_string('email_template.html', {
            'nombre': contacto.nombre,
            'email': contacto.email,
            'mensaje': contacto.mensaje,
        })
        
        # Crear el correo electrónico
        email = EmailMultiAlternatives(subject, contacto.mensaje, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        
        try:
            email.send()
        except Exception as e:
            logger.error(f'Error al enviar el correo: {e}')
            raise