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