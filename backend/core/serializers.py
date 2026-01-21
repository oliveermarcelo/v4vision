from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Company

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    """Serializer para Company"""
    users_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'slug', 'logo', 'primary_color', 
            'is_active', 'users_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_users_count(self, obj):
        return obj.users.count()


class CompanyMinimalSerializer(serializers.ModelSerializer):
    """Serializer mínimo para Company (usado em listagens)"""
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'slug', 'logo', 'primary_color']


class UserSerializer(serializers.ModelSerializer):
    """Serializer para User"""
    company_data = CompanyMinimalSerializer(source='company', read_only=True)
    full_name = serializers.SerializerMethodField()
    can_edit = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'company', 'company_data', 'role', 'avatar', 
            'can_edit', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'company': {'write_only': True}
        }
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de User"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'company', 'role'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'As senhas não coincidem.'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para troca de senha"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Senha atual incorreta.')
        return value


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    email = serializers.EmailField()
    password = serializers.CharField()
