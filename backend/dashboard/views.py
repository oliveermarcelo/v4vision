from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F, Max
from django.db.models.functions import Coalesce

from core.permissions import CanEditOrReadOnly
from .models import (
    Vendedor, ReceitaMensal, VendaVendedor,
    Estrategia, InvestimentoMensal, GestaoSemanal, Protocolo
)
from .serializers import (
    VendedorSerializer, ReceitaMensalSerializer, VendaVendedorSerializer,
    EstrategiaSerializer, EstrategiaCreateSerializer, GestaoSemanalSerializer,
    ProtocoloSerializer
)


class CompanyFilterMixin:
    """Mixin para filtrar queryset por empresa do usuário"""
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        # Platform admin vê tudo
        if user.is_platform_admin:
            company_id = self.request.query_params.get('company')
            if company_id:
                return qs.filter(company_id=company_id)
            return qs
        
        # Outros usuários veem apenas sua empresa
        if user.company:
            return qs.filter(company=user.company)
        
        return qs.none()
    
    def perform_create(self, serializer):
        """Adiciona company automaticamente ao criar"""
        user = self.request.user
        company = user.company
        
        # Platform admin pode especificar company
        if user.is_platform_admin:
            company_id = self.request.data.get('company')
            if company_id:
                from core.models import Company
                company = Company.objects.get(id=company_id)
        
        serializer.save(company=company)


class VendedorViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    """ViewSet para Vendedores"""
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    permission_classes = [CanEditOrReadOnly]
    filterset_fields = ['is_active']


class ReceitaMensalViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    """ViewSet para Receita Mensal"""
    queryset = ReceitaMensal.objects.all()
    serializer_class = ReceitaMensalSerializer
    permission_classes = [CanEditOrReadOnly]
    filterset_fields = ['ano', 'mes']
    
    @action(detail=False, methods=['get'])
    def retrospectiva(self, request):
        """Retorna dados da retrospectiva anual"""
        ano = request.query_params.get('ano', 2025)
        qs = self.get_queryset().filter(ano=ano)
        
        # Totais
        totais = qs.aggregate(
            receita_total=Coalesce(Sum('receita'), 0),
            investimento_total=Coalesce(Sum('investimento'), 0),
            leads_total=Coalesce(Sum('leads'), 0)
        )
        
        # ROAS global
        roas_global = 0
        if totais['investimento_total'] > 0:
            roas_global = float(totais['receita_total'] / totais['investimento_total'])
        
        # Mês de pico
        mes_pico = qs.order_by('-receita').first()
        mes_pico_data = None
        if mes_pico:
            mes_pico_data = {
                'mes': mes_pico.mes,
                'mes_nome': mes_pico.get_mes_display(),
                'receita': float(mes_pico.receita)
            }
        
        # Dados mensais
        receitas_mensais = ReceitaMensalSerializer(qs.order_by('mes'), many=True).data
        
        return Response({
            'ano': ano,
            'receita_total': totais['receita_total'],
            'investimento_total': totais['investimento_total'],
            'roas_global': round(roas_global, 2),
            'leads_total': totais['leads_total'],
            'mes_pico': mes_pico_data,
            'receitas_mensais': receitas_mensais
        })
    
    @action(detail=False, methods=['get'])
    def comparativo_vendedores(self, request):
        """Retorna comparativo de vendas por vendedor"""
        ano = request.query_params.get('ano', 2025)
        user = request.user
        
        # Filtra por empresa
        if user.is_platform_admin:
            company_id = request.query_params.get('company')
            vendas = VendaVendedor.objects.filter(ano=ano)
            if company_id:
                vendas = vendas.filter(company_id=company_id)
        else:
            vendas = VendaVendedor.objects.filter(
                company=user.company,
                ano=ano
            )
        
        # Agrupa por vendedor
        comparativo = vendas.values(
            'vendedor__nome'
        ).annotate(
            total=Sum('valor')
        ).order_by('-total')
        
        result = [
            {'vendedor': item['vendedor__nome'], 'total': item['total']}
            for item in comparativo
        ]
        
        return Response(result)


class VendaVendedorViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    """ViewSet para Vendas por Vendedor"""
    queryset = VendaVendedor.objects.all()
    serializer_class = VendaVendedorSerializer
    permission_classes = [CanEditOrReadOnly]
    filterset_fields = ['vendedor', 'ano', 'mes']


class EstrategiaViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    """ViewSet para Estratégia"""
    queryset = Estrategia.objects.all()
    permission_classes = [CanEditOrReadOnly]
    filterset_fields = ['ano', 'cenario']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EstrategiaCreateSerializer
        return EstrategiaSerializer
    
    @action(detail=True, methods=['post'])
    def set_investimentos(self, request, pk=None):
        """Define investimentos mensais da estratégia"""
        estrategia = self.get_object()
        investimentos = request.data.get('investimentos', [])
        
        # Remove investimentos antigos
        estrategia.investimentos_mensais.all().delete()
        
        # Cria novos
        for inv in investimentos:
            InvestimentoMensal.objects.create(
                estrategia=estrategia,
                mes=inv['mes'],
                valor=inv['valor']
            )
        
        serializer = EstrategiaSerializer(estrategia)
        return Response(serializer.data)


class GestaoSemanalViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    """ViewSet para Gestão Semanal"""
    queryset = GestaoSemanal.objects.all()
    serializer_class = GestaoSemanalSerializer
    permission_classes = [CanEditOrReadOnly]
    filterset_fields = ['ano', 'mes', 'semana']


class ProtocoloViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    """ViewSet para Protocolos"""
    queryset = Protocolo.objects.all()
    serializer_class = ProtocoloSerializer
    permission_classes = [CanEditOrReadOnly]
    filterset_fields = ['tipo']
