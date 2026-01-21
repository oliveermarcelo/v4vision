from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import Company
from .serializers import (
    CompanySerializer, UserSerializer, UserCreateSerializer,
    ChangePasswordSerializer
)
from .permissions import IsPlatformAdmin, IsCompanyAdmin, CanEditOrReadOnly

User = get_user_model()


class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de empresas"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Platform admin vê todas, outros veem só a sua
            return [IsAuthenticated()]
        return [IsPlatformAdmin()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_platform_admin:
            return Company.objects.all()
        # Usuário comum só vê sua própria empresa
        if user.company:
            return Company.objects.filter(id=user.company.id)
        return Company.objects.none()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de usuários"""
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['me', 'change_password']:
            return [IsAuthenticated()]
        if self.action in ['list', 'retrieve']:
            return [IsCompanyAdmin()]
        return [IsPlatformAdmin()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_platform_admin:
            return User.objects.all()
        # Admin da empresa vê usuários da sua empresa
        if user.is_company_admin and user.company:
            return User.objects.filter(company=user.company)
        # Usuário comum não lista outros
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """Retorna ou atualiza dados do usuário logado"""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Altera senha do usuário logado"""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({'message': 'Senha alterada com sucesso.'})


class RegisterView(generics.CreateAPIView):
    """View para registro de novos usuários (apenas platform admin)"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsPlatformAdmin]


class LogoutView(generics.GenericAPIView):
    """View para logout (blacklist do refresh token)"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logout realizado com sucesso.'})
        except Exception:
            return Response(
                {'error': 'Token inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
