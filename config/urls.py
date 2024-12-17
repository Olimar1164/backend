from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from contactos.views import ContactoViewSet, UserViewSet, get_csrf_token, CustomTokenObtainPairView, CustomTokenRefreshView

router = DefaultRouter()
router.register(r'contactos', ContactoViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/csrf/', get_csrf_token, name='get-csrf-token'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]