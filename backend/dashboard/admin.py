from django.contrib import admin
from .models import (
    Vendedor, ReceitaMensal, VendaVendedor,
    Estrategia, InvestimentoMensal, GestaoSemanal, Protocolo
)


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'company', 'email', 'is_active']
    list_filter = ['company', 'is_active']
    search_fields = ['nome', 'email']


@admin.register(ReceitaMensal)
class ReceitaMensalAdmin(admin.ModelAdmin):
    list_display = ['company', 'ano', 'mes', 'receita', 'investimento', 'leads']
    list_filter = ['company', 'ano', 'mes']
    ordering = ['-ano', '-mes']


@admin.register(VendaVendedor)
class VendaVendedorAdmin(admin.ModelAdmin):
    list_display = ['vendedor', 'company', 'ano', 'mes', 'valor']
    list_filter = ['company', 'ano', 'mes']
    ordering = ['-ano', '-mes']


class InvestimentoMensalInline(admin.TabularInline):
    model = InvestimentoMensal
    extra = 0


@admin.register(Estrategia)
class EstrategiaAdmin(admin.ModelAdmin):
    list_display = ['company', 'ano', 'cenario', 'orcamento_total', 'receita_projetada']
    list_filter = ['company', 'ano', 'cenario']
    inlines = [InvestimentoMensalInline]


@admin.register(GestaoSemanal)
class GestaoSemanalAdmin(admin.ModelAdmin):
    list_display = ['company', 'ano', 'mes', 'semana', 'investimento', 'leads', 'vendas']
    list_filter = ['company', 'ano', 'mes']
    ordering = ['-ano', '-mes', '-semana']


@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    list_display = ['company', 'tipo', 'titulo', 'ordem']
    list_filter = ['company', 'tipo']
    ordering = ['company', 'ordem']
