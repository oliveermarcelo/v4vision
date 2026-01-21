from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core.views import CompanyViewSet, UserViewSet, RegisterView, LogoutView
from dashboard.views import (
    VendedorViewSet, ReceitaMensalViewSet, VendaVendedorViewSet,
    EstrategiaViewSet, GestaoSemanalViewSet, ProtocoloViewSet
)

# Router da API
router = DefaultRouter()

# Core
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'users', UserViewSet, basename='user')

# Dashboard
router.register(r'vendedores', VendedorViewSet, basename='vendedor')
router.register(r'receitas', ReceitaMensalViewSet, basename='receita')
router.register(r'vendas-vendedor', VendaVendedorViewSet, basename='venda-vendedor')
router.register(r'estrategias', EstrategiaViewSet, basename='estrategia')
router.register(r'gestao-semanal', GestaoSemanalViewSet, basename='gestao-semanal')
router.register(r'protocolos', ProtocoloViewSet, basename='protocolo')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include(router.urls)),
    
    # Auth
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
