from rest_framework import permissions


class IsPlatformAdmin(permissions.BasePermission):
    """Permite acesso apenas para admins da plataforma"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.is_platform_admin
        )


class IsCompanyAdmin(permissions.BasePermission):
    """Permite acesso para admins da empresa ou plataforma"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.is_company_admin
        )


class IsCompanyAdminOrReadOnly(permissions.BasePermission):
    """
    Admin da empresa pode editar, outros apenas visualizam
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Leitura liberada para todos autenticados
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Escrita apenas para admins
        return request.user.is_company_admin


class IsSameCompany(permissions.BasePermission):
    """Verifica se o usuário pertence à mesma empresa do objeto"""
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Platform admin pode acessar qualquer empresa
        if request.user.is_platform_admin:
            return True
        
        # Verifica se o objeto tem company e se é a mesma do usuário
        if hasattr(obj, 'company'):
            return obj.company == request.user.company
        
        # Se o objeto É uma company, verifica se é a do usuário
        if hasattr(obj, 'users'):  # É uma Company
            return obj == request.user.company
        
        return False


class CanEditOrReadOnly(permissions.BasePermission):
    """
    Usuários com can_edit podem modificar, outros apenas leem.
    Também verifica se pertence à mesma empresa.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.can_edit
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Platform admin pode tudo
        if request.user.is_platform_admin:
            return True
        
        # Verifica mesma empresa
        if hasattr(obj, 'company'):
            if obj.company != request.user.company:
                return False
        
        # Leitura sempre permitida para mesma empresa
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Escrita apenas para quem pode editar
        return request.user.can_edit
