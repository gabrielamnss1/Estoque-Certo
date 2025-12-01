# financeiro.py
# ============================================================================
# MÓDULO 3: FINANCEIRO - CÁLCULO DE CUSTOS E LUCROS
# ============================================================================
# Este módulo calcula os custos operacionais mensais, define preço de venda
# com base em margem de lucro e projeta faturamento e lucros.
# 
# CONCEITOS DEMONSTRADOS:
# - Entrada de dados tipo float (números decimais)
# - Operações matemáticas (soma, divisão, multiplicação)
# - Cálculo de porcentagens e margens
# - Formatação de valores monetários
# - Projeções financeiras
# ============================================================================

# ============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA PURA)
# ============================================================================

def calcular_metricas_financeiras(agua, luz, impostos, salarios, total_pallets=1000):
    """Realiza todos os cálculos financeiros e retorna um dicionário com os resultados"""
    custo_total = agua + luz + impostos + salarios
    custo_por_pallet = custo_total / total_pallets if total_pallets > 0 else 0
    
    margem_lucro = 0.50
    preco_venda = custo_por_pallet * (1 + margem_lucro)
    lucro_por_unidade = preco_venda - custo_por_pallet
    
    receita_mensal = preco_venda * total_pallets
    lucro_mensal = lucro_por_unidade * total_pallets
    
    receita_anual = receita_mensal * 12
    lucro_anual = lucro_mensal * 12
    
    margem_lucro_real = (lucro_mensal / receita_mensal * 100) if receita_mensal > 0 else 0
    ponto_equilibrio = custo_total / lucro_por_unidade if lucro_por_unidade > 0 else 0
    roi = (lucro_mensal / custo_total * 100) if custo_total > 0 else 0
    
    return {
        "custo_total": custo_total,
        "custo_por_pallet": custo_por_pallet,
        "preco_venda": preco_venda,
        "lucro_por_unidade": lucro_por_unidade,
        "receita_mensal": receita_mensal,
        "lucro_mensal": lucro_mensal,
        "receita_anual": receita_anual,
        "lucro_anual": lucro_anual,
        "margem_lucro_real": margem_lucro_real,
        "ponto_equilibrio": ponto_equilibrio,
        "roi": roi,
        "margem_lucro_alvo": margem_lucro
    }