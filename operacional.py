# operacional.py
# ============================================================================
# MÓDULO 1: OPERACIONAL - CÁLCULO DE CAPACIDADE DE PRODUÇÁO
# ============================================================================
# Este módulo é responsável por calcular a capacidade de produção da fábrica
# com base no número de turnos ativos (Manhã, Tarde e/ou Noite).
# 
# CONCEITOS DEMONSTRADOS:
# - Entrada e validação de dados
# - Operações matemáticas básicas (multiplicação)
# - Estruturas condicionais (if/else)
# - Formatação de saída de dados
# ============================================================================

# ============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA PURA)
# ============================================================================

def calcular_metricas_capacidade(turnos):
    """Calcula as métricas de capacidade baseada nos turnos"""
    capacidade_por_turno = 1666
    capacidade_diaria = capacidade_por_turno * turnos
    capacidade_mensal = capacidade_diaria * 30
    capacidade_anual = capacidade_mensal * 12
    
    capacidade_maxima_diaria = capacidade_por_turno * 3
    diferenca = capacidade_maxima_diaria - capacidade_diaria
    percentual_uso = (capacidade_diaria / capacidade_maxima_diaria) * 100
    