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