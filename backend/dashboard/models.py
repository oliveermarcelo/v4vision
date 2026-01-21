from django.db import models
from django.core.validators import MinValueValidator
from core.models import Company
import uuid


class BaseModel(models.Model):
    """Modelo base com campos comuns"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        abstract = True


class Vendedor(BaseModel):
    """Vendedores da empresa"""
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='vendedores',
        verbose_name='Empresa'
    )
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email', blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    
    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering = ['nome']
        unique_together = ['company', 'email']
    
    def __str__(self):
        return self.nome


class ReceitaMensal(BaseModel):
    """Receita mensal da empresa"""
    
    class Mes(models.IntegerChoices):
        JANEIRO = 1, 'Janeiro'
        FEVEREIRO = 2, 'Fevereiro'
        MARCO = 3, 'Março'
        ABRIL = 4, 'Abril'
        MAIO = 5, 'Maio'
        JUNHO = 6, 'Junho'
        JULHO = 7, 'Julho'
        AGOSTO = 8, 'Agosto'
        SETEMBRO = 9, 'Setembro'
        OUTUBRO = 10, 'Outubro'
        NOVEMBRO = 11, 'Novembro'
        DEZEMBRO = 12, 'Dezembro'
    
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='receitas_mensais',
        verbose_name='Empresa'
    )
    ano = models.PositiveIntegerField('Ano')
    mes = models.PositiveSmallIntegerField('Mês', choices=Mes.choices)
    receita = models.DecimalField(
        'Receita', 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    investimento = models.DecimalField(
        'Investimento', 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    leads = models.PositiveIntegerField('Leads', default=0)
    
    class Meta:
        verbose_name = 'Receita Mensal'
        verbose_name_plural = 'Receitas Mensais'
        ordering = ['-ano', '-mes']
        unique_together = ['company', 'ano', 'mes']
    
    def __str__(self):
        return f"{self.company.name} - {self.get_mes_display()}/{self.ano}"
    
    @property
    def roas(self):
        """Calcula ROAS (Return on Ad Spend)"""
        if self.investimento and self.investimento > 0:
            return float(self.receita / self.investimento)
        return 0


class VendaVendedor(BaseModel):
    """Vendas por vendedor"""
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='vendas_vendedor',
        verbose_name='Empresa'
    )
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE,
        related_name='vendas',
        verbose_name='Vendedor'
    )
    ano = models.PositiveIntegerField('Ano')
    mes = models.PositiveSmallIntegerField('Mês', choices=ReceitaMensal.Mes.choices)
    valor = models.DecimalField(
        'Valor', 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        verbose_name = 'Venda por Vendedor'
        verbose_name_plural = 'Vendas por Vendedor'
        ordering = ['-ano', '-mes', 'vendedor__nome']
        unique_together = ['company', 'vendedor', 'ano', 'mes']
    
    def __str__(self):
        return f"{self.vendedor.nome} - {self.get_mes_display()}/{self.ano}"


class Estrategia(BaseModel):
    """Estratégia/Planejamento da empresa"""
    
    class Cenario(models.TextChoices):
        CONSERVADOR = 'conservador', 'Conservador'
        OUSADO = 'ousado', 'Ousado'
    
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='estrategias',
        verbose_name='Empresa'
    )
    ano = models.PositiveIntegerField('Ano')
    cenario = models.CharField(
        'Cenário',
        max_length=20,
        choices=Cenario.choices,
        default=Cenario.CONSERVADOR
    )
    orcamento_total = models.DecimalField(
        'Orçamento Total',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    receita_projetada = models.DecimalField(
        'Receita Projetada',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    roas_minimo = models.DecimalField(
        'ROAS Mínimo',
        max_digits=5,
        decimal_places=2,
        default=4.0,
        help_text='Se ROAS < este valor, congelar investimento'
    )
    
    class Meta:
        verbose_name = 'Estratégia'
        verbose_name_plural = 'Estratégias'
        ordering = ['-ano']
        unique_together = ['company', 'ano', 'cenario']
    
    def __str__(self):
        return f"{self.company.name} - {self.ano} ({self.get_cenario_display()})"


class InvestimentoMensal(BaseModel):
    """Investimento mensal planejado na estratégia"""
    estrategia = models.ForeignKey(
        Estrategia,
        on_delete=models.CASCADE,
        related_name='investimentos_mensais',
        verbose_name='Estratégia'
    )
    mes = models.PositiveSmallIntegerField('Mês', choices=ReceitaMensal.Mes.choices)
    valor = models.DecimalField(
        'Valor',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        verbose_name = 'Investimento Mensal'
        verbose_name_plural = 'Investimentos Mensais'
        ordering = ['mes']
        unique_together = ['estrategia', 'mes']
    
    def __str__(self):
        return f"{self.estrategia} - {self.get_mes_display()}"


class GestaoSemanal(BaseModel):
    """Registro semanal de métricas"""
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='gestao_semanal',
        verbose_name='Empresa'
    )
    ano = models.PositiveIntegerField('Ano')
    mes = models.PositiveSmallIntegerField('Mês', choices=ReceitaMensal.Mes.choices)
    semana = models.PositiveSmallIntegerField('Semana', choices=[
        (1, 'Semana 1'),
        (2, 'Semana 2'),
        (3, 'Semana 3'),
        (4, 'Semana 4'),
        (5, 'Semana 5'),
    ])
    investimento = models.DecimalField(
        'Investimento',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    leads = models.PositiveIntegerField('Leads')
    vendas = models.DecimalField(
        'Vendas',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        verbose_name = 'Gestão Semanal'
        verbose_name_plural = 'Gestões Semanais'
        ordering = ['-ano', '-mes', '-semana']
        unique_together = ['company', 'ano', 'mes', 'semana']
    
    def __str__(self):
        return f"{self.company.name} - {self.get_mes_display()}/{self.ano} - Semana {self.semana}"
    
    @property
    def roas(self):
        if self.investimento and self.investimento > 0:
            return float(self.vendas / self.investimento)
        return 0


class Protocolo(BaseModel):
    """Protocolos operacionais da empresa"""
    
    class Tipo(models.TextChoices):
        SLA = 'sla', 'SLA'
        FOCO = 'foco', 'Foco'
        FEEDBACK = 'feedback', 'Feedback'
        OUTRO = 'outro', 'Outro'
    
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='protocolos',
        verbose_name='Empresa'
    )
    tipo = models.CharField('Tipo', max_length=20, choices=Tipo.choices)
    titulo = models.CharField('Título', max_length=100)
    descricao = models.TextField('Descrição')
    icone = models.CharField('Ícone', max_length=50, blank=True, help_text='Nome do ícone Lucide')
    cor = models.CharField('Cor', max_length=20, default='orange')
    ordem = models.PositiveSmallIntegerField('Ordem', default=0)
    
    class Meta:
        verbose_name = 'Protocolo'
        verbose_name_plural = 'Protocolos'
        ordering = ['ordem', 'tipo']
    
    def __str__(self):
        return f"{self.company.name} - {self.titulo}"
