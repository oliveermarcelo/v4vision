from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid


class Company(models.Model):
    """Modelo de empresa para multi-tenancy"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Nome da Empresa', max_length=200)
    slug = models.SlugField('Slug', unique=True, max_length=100)
    logo = models.ImageField('Logo', upload_to='companies/logos/', blank=True, null=True)
    primary_color = models.CharField('Cor Primária', max_length=7, default='#F97316')
    is_active = models.BooleanField('Ativa', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """Manager customizado para User"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.PLATFORM_ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User customizado com roles e vínculo com empresa"""
    
    class Role(models.TextChoices):
        PLATFORM_ADMIN = 'platform_admin', 'Admin da Plataforma'
        COMPANY_ADMIN = 'company_admin', 'Admin da Empresa'
        VIEWER = 'viewer', 'Visualizador'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # Remove username, usamos email
    email = models.EmailField('Email', unique=True)
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='users',
        verbose_name='Empresa',
        null=True, 
        blank=True
    )
    role = models.CharField(
        'Função',
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER
    )
    avatar = models.ImageField('Avatar', upload_to='users/avatars/', blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    @property
    def is_platform_admin(self):
        return self.role == self.Role.PLATFORM_ADMIN
    
    @property
    def is_company_admin(self):
        return self.role in [self.Role.PLATFORM_ADMIN, self.Role.COMPANY_ADMIN]
    
    @property
    def can_edit(self):
        """Verifica se o usuário pode editar dados"""
        return self.role in [self.Role.PLATFORM_ADMIN, self.Role.COMPANY_ADMIN]
