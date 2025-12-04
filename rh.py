# rh.py
# ============================================================================
# MÓDULO 4: RECURSOS HUMANOS - FOLHA DE PAGAMENTO
# ============================================================================
# Este módulo calcula a folha de pagamento com salários, horas extras,
# INSS e Imposto de Renda de acordo com as tabelas de 2025.
# 
# CONCEITOS DEMONSTRADOS:
# - Estruturas condicionais complexas (if/elif/else)
# - Cálculo de impostos progressivos
# - Ordenação de listas (sort com lambda)
# - Manipulação de dicionários
# - Validação de dados
# - Formatação de relatórios
# ============================================================================

# ============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA PURA)
# ============================================================================

def calcular_inss(salario_bruto):
    """Calcula o desconto do INSS baseado na tabela progressiva de 2025"""
    if salario_bruto <= 1412.00:
        return salario_bruto * 0.075
    elif salario_bruto <= 2666.68:
        return salario_bruto * 0.09
    elif salario_bruto <= 4000.03:
        return salario_bruto * 0.12
    else:
        desconto = salario_bruto * 0.14
        return min(desconto, 908.85) # Teto do INSS

def calcular_ir(base_calculo):
    """Calcula o desconto do IR baseado na tabela progressiva de 2025"""
    if base_calculo <= 2259.20:
        return 0.0
    elif base_calculo <= 2826.65:
        return (base_calculo * 0.075) - 169.44
    elif base_calculo <= 3751.05:
        return (base_calculo * 0.15) - 381.44
    elif base_calculo <= 4664.68:
        return (base_calculo * 0.225) - 662.77
    else:
        return (base_calculo * 0.275) - 896.00

def processar_funcionario(nome, cargo, horas_extras):
    """Processa os cálculos completos para um funcionário"""
    tabela_cargos = {
        'Operário': {'valor_hora': 15.00, 'paga_he': True},
        'Supervisor': {'valor_hora': 40.00, 'paga_he': True},
        'Gerente': {'valor_hora': 60.00, 'paga_he': False},
        'Diretor': {'valor_hora': 80.00, 'paga_he': False}
    }
    
    dados_cargo = tabela_cargos.get(cargo, tabela_cargos['Operário'])
    valor_hora = dados_cargo['valor_hora']
    paga_he = dados_cargo['paga_he']
    
    salario_bruto = 160 * valor_hora
    valor_extras = 0.0
    
    if paga_he and horas_extras > 0:
        valor_extras = horas_extras * (valor_hora * 2)
        salario_bruto += valor_extras
        
    desconto_inss = calcular_inss(salario_bruto)
    base_ir = salario_bruto - desconto_inss
    desconto_ir = max(0, calcular_ir(base_ir))
    salario_liquido = salario_bruto - desconto_inss - desconto_ir
    
    return {
        "nome": nome,
        "cargo": cargo,
        "valor_hora": valor_hora,
        "horas_extras": horas_extras,
        "bruto": salario_bruto,
        "extras": valor_extras,
        "inss": desconto_inss,
        "ir": desconto_ir,
        "liquido": salario_liquido
    }

def calcular_folha_pagamento():
    """
    Calcula a folha de pagamento completa com descontos de INSS e IR.
    
    Esta função demonstra conceitos de:
    - Cálculo de impostos progressivos (faixas diferentes de alíquota)
    - Estruturas condicionais complexas (if/elif/else encadeados)
    - Manipulação de listas de dicionários
    - Ordenação de dados (sort com lambda)
    - Totalização e agregação de dados
    - Cálculo de horas extras (valor dobrado)
    
    MODO: Interativo para console
    """

    
    print("\n" + "="*50)
    print("   MODULO 4: RECURSOS HUMANOS - FOLHA DE PAGAMENTO")
    print("="*50)
    
    # Lista para armazenar os dados de todos os funcionários processados
    lista_funcionarios = []
    
    # ========================================================================
    # PASSO 1: DEFINIR QUANTOS FUNCIONÁRIOS SERÁO CALCULADOS
    # ========================================================================
    try:
        qtd = int(input("\n Quantos funcionarios vai calcular? "))
        
        # Validação: não aceita valores zero ou negativos
        if qtd <= 0:
            print("\n Quantidade deve ser maior que zero!")
            return
            
    except ValueError:
        # Tratamento de erro para entradas não numéricas
        print("\n Erro: Digite apenas numeros inteiros!")
        return

    # ========================================================================
    # PASSO 2: LOOP PARA CADASTRAR CADA FUNCIONÁRIO
    # ========================================================================
    for i in range(qtd):
        print("\n" + "-"*50)
        print(f" FUNCIONARIO {i+1} DE {qtd}")
        print("-"*50)
        
        # ====================================================================
        # PASSO 2.1: COLETAR DADOS BÁSICOS
        # ====================================================================
        nome = input(" Nome completo: ").strip()
        
        # Validação: nome é obrigatório
        if not nome:
            print(" Nome nao pode estar vazio! Pulando este funcionario.")
            continue  # Pula para a próxima iteração do loop
        
        # Exibe as opções de cargos disponíveis
        print("\n Cargos disponiveis:")
        print("   1 - Operario")
        print("   2 - Supervisor")
        print("   3 - Gerente")
        print("   4 - Diretor")
        
        cargo_opcao = input("Escolha o cargo (1-4): ").strip()