from rest_framework import serializers
from .models import (
    Vendedor, ReceitaMensal, VendaVendedor, 
    Estrategia, InvestimentoMensal, GestaoSemanal, Protocolo
)


class VendedorSerializer(serializers.ModelSerializer):
    total_vendas = serializers.SerializerMethodField()
    
    class Meta:
        model = Vendedor
        fields = ['id', 'nome', 'email', 'is_active', 'total_vendas', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_total_vendas(self, obj):
        # Soma todas as vendas do vendedor
        total = obj.vendas.aggregate(total=models.Sum('valor'))['total']
        return float(total) if total else 0


class ReceitaMensalSerializer(serializers.ModelSerializer):
    mes_nome = serializers.CharField(source='get_mes_display', read_only=True)
    roas = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ReceitaMensal
        fields = [
            'id', 'ano', 'mes', 'mes_nome', 'receita', 
            'investimento', 'leads', 'roas', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class VendaVendedorSerializer(serializers.ModelSerializer):
    vendedor_nome = serializers.CharField(source='vendedor.nome', read_only=True)
    mes_nome = serializers.CharField(source='get_mes_display', read_only=True)
    
    class Meta:
        model = VendaVendedor
        fields = [
            'id', 'vendedor', 'vendedor_nome', 'ano', 
            'mes', 'mes_nome', 'valor', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class InvestimentoMensalSerializer(serializers.ModelSerializer):
    mes_nome = serializers.CharField(source='get_mes_display', read_only=True)
    
    class Meta:
        model = InvestimentoMensal
        fields = ['id', 'mes', 'mes_nome', 'valor']
        read_only_fields = ['id']


class EstrategiaSerializer(serializers.ModelSerializer):
    cenario_nome = serializers.CharField(source='get_cenario_display', read_only=True)
    investimentos_mensais = InvestimentoMensalSerializer(many=True, read_only=True)
    
    class Meta:
        model = Estrategia
        fields = [
            'id', 'ano', 'cenario', 'cenario_nome', 'orcamento_total',
            'receita_projetada', 'roas_minimo', 'investimentos_mensais', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class EstrategiaCreateSerializer(serializers.ModelSerializer):
    investimentos = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Estrategia
        fields = [
            'ano', 'cenario', 'orcamento_total',
            'receita_projetada', 'roas_minimo', 'investimentos'
        ]
    
    def create(self, validated_data):
        investimentos_data = validated_data.pop('investimentos', [])
        estrategia = Estrategia.objects.create(**validated_data)
        
        for inv in investimentos_data:
            InvestimentoMensal.objects.create(
                estrategia=estrategia,
                mes=inv['mes'],
                valor=inv['valor']
            )
        
        return estrategia


class GestaoSemanalSerializer(serializers.ModelSerializer):
    mes_nome = serializers.CharField(source='get_mes_display', read_only=True)
    semana_nome = serializers.CharField(source='get_semana_display', read_only=True)
    roas = serializers.FloatField(read_only=True)
    
    class Meta:
        model = GestaoSemanal
        fields = [
            'id', 'ano', 'mes', 'mes_nome', 'semana', 'semana_nome',
            'investimento', 'leads', 'vendas', 'roas', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProtocoloSerializer(serializers.ModelSerializer):
    tipo_nome = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Protocolo
        fields = [
            'id', 'tipo', 'tipo_nome', 'titulo', 
            'descricao', 'icone', 'cor', 'ordem'
        ]
        read_only_fields = ['id']


# Serializers para Dashboard/Retrospectiva
class RetrospectivaSummarySerializer(serializers.Serializer):
    """Resumo da retrospectiva anual"""
    receita_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    investimento_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    roas_global = serializers.FloatField()
    leads_total = serializers.IntegerField()
    mes_pico = serializers.DictField()
    receitas_mensais = ReceitaMensalSerializer(many=True)


class ComparativoVendedoresSerializer(serializers.Serializer):
    """Comparativo de vendas por vendedor"""
    vendedor = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)


# Import para aggregate
from django.db import models
