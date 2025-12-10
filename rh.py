# -*- coding: utf-8 -*-
# rh.py
# ============================================================================
# ARQUIVO: main.py
# SISTEMA DE GESTÃO - QUATRO CANTOS
# ============================================================================
#
# DESCRIÇÃO:
# Este é o arquivo principal do sistema em modo console/terminal.
# Ele gerencia o menu interativo e permite que o usuário navegue entre
# os diferentes módulos do sistema através de opções numeradas.
#
# FUNCIONALIDADES:
# 1. Exibir menu principal com todas as opções disponíveis
# 2. Capturar a escolha do usuário
# 3. Redirecionar para o módulo correspondente
# 4. Manter o sistema em loop até o usuário decidir sair
# 5. Gerenciar conexão com o banco de dados
#
# MÓDULOS INTEGRADOS:
# - Operacional: Cálculo de capacidade produtiva
# - Estoque Entrada: Cadastro de produtos recebidos
# - Estoque Saída: Registro de vendas e saídas
# - Financeiro: Análise de custos e lucros
# - RH: Gestão de folha de pagamento
#
# ============================================================================

# Configurar encoding UTF-8 para Windows
import config_encoding

# ============================================================================
# IMPORTAÇÃO DOS MÓDULOS CUSTOMIZADOS DO SISTEMA
# ============================================================================
# Cada módulo representa uma funcionalidade específica do sistema
import operacional       # Módulo para cálculos operacionais e produtivos
import estoque_entrada   # Módulo para entrada de produtos no estoque
import estoque_saida     # Módulo para saída/venda de produtos
import financeiro        # Módulo para análises financeiras
import rh                # Módulo de Recursos Humanos (RH)
from database import init_db, SessionLocal  # Funções para gerenciar o banco de dados

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

def iniciar_sistema():
    """
    Função principal que inicializa e gerencia todo o sistema.
    
    Esta função demonstra conceitos de:
    - Cálculo de impostos progressivos (faixas diferentes de alíquota)
    - Estruturas condicionais complexas (if/elif/else encadeados)
    - Manipulação de listas de dicionários
    - Ordenação de dados (sort com lambda)
    - Totalização e agregação de dados
    - Cálculo de horas extras (valor dobrado - 100% de acréscimo)
    
    FUNCIONAMENTO:
    - O sistema roda em um loop infinito (while True)
    - A cada iteração, exibe o menu e aguarda entrada do usuário
    - Executa a ação correspondente à opção escolhida
    - Só encerra quando o usuário escolhe a opção '0'
    """

    
    print("\n" + "="*70)
    print("   MÓDULO 4: RECURSOS HUMANOS - FOLHA DE PAGAMENTO")
    print("="*70)
    
    # Lista para armazenar os dados de todos os funcionários processados
    lista_funcionarios = []
    
    # ========================================================================
    # PASSO 1: DEFINIR QUANTOS FUNCIONÁRIOS SERÃO CALCULADOS
    # ========================================================================
    try:
        qtd = int(input("\nQuantos funcionários vai calcular? "))
        
        # Validação: não aceita valores zero ou negativos
        if qtd <= 0:
            print("\nQuantidade deve ser maior que zero!")
            return
            
    except ValueError:
        # Tratamento de erro para entradas não numéricas
        print("\nErro: Digite apenas números inteiros!")
        return
    
    # ========================================================================
    # CRIAÇÃO DA SESSÃO DO BANCO DE DADOS
    # ========================================================================
    for i in range(qtd):
        print("\n" + "="*70)
        print(f"   FUNCIONÁRIO {i+1} DE {qtd}")
        print("="*70)
        
        # ====================================================================
        # PASSO 2.1: COLETAR DADOS BÁSICOS
        # ====================================================================
        nome = input("\nNome completo: ").strip()
        
        # Validação: nome é obrigatório
        if not nome:
            print("\n[ERRO] Nome não pode estar vazio! Pulando este funcionário.")
            continue  # Pula para a próxima iteração do loop
        
        # Exibe as opções de cargos disponíveis
        print("\nCargos disponíveis:")
        print("   1 - Operário      (R$ 15,00/h - Recebe Hora Extra)")
        print("   2 - Supervisor    (R$ 40,00/h - Recebe Hora Extra)")
        print("   3 - Gerente       (R$ 60,00/h - Cargo de Confiança)")
        print("   4 - Diretor       (R$ 80,00/h - Cargo de Confiança)")
        
        cargo_opcao = input("\n➤ Escolha o cargo (1-4): ").strip()
        
        # ====================================================================
        # LOOP PRINCIPAL DO SISTEMA
        # ====================================================================
        # Cada cargo tem um valor/hora diferente e regras diferentes para HE
        valor_hora = 0
        paga_hora_extra = False
        cargo = ""
        
        # Estrutura condicional para definir valores conforme o cargo escolhido
        if cargo_opcao == "1":
            cargo = "Operário"
            valor_hora = 15.00
            paga_hora_extra = True  # Operário TEM DIREITO a hora extra
            print("\n[OK] Cargo: Operário - Elegível para Horas Extras")
            
        elif cargo_opcao == "2":
            cargo = "Supervisor"
            valor_hora = 40.00
            paga_hora_extra = True  # Supervisor TEM DIREITO a hora extra
            print("\n[OK] Cargo: Supervisor - Elegível para Horas Extras")
            
        elif cargo_opcao == "3":
            cargo = "Gerente"
            valor_hora = 60.00
            paga_hora_extra = False  # Gerente NÁO RECEBE hora extra (cargo de confiança)
            print("\n[OK] Cargo: Gerente - Cargo de Confiança (sem hora extra)")
            
        elif cargo_opcao == "4":
            cargo = "Diretor"
            valor_hora = 80.00
            paga_hora_extra = False  # Diretor NÁO RECEBE hora extra (cargo de confiança)
            print("\n[OK] Cargo: Diretor - Cargo de Confiança (sem hora extra)")
            
        else:
            # Opção inválida: usa valores padrão
            print("\n[AVISO] Cargo inválido! Usando Operário como padrão.")
            cargo = "Operário"
            valor_hora = 15.00
            paga_hora_extra = True
        
        # ====================================================================
        # PASSO 2.2.1: COLETAR HORAS EXTRAS (SE APLICÁVEL)
        # ====================================================================
        horas_extras = 0
        if paga_hora_extra:
            print("\nHORAS EXTRAS (Acréscimo de 100% sobre o valor/hora):")
            try:
                horas_extras = float(input("   Digite as horas extras trabalhadas no mês: "))
                if horas_extras < 0:
                    print("   [AVISO] Valor negativo ajustado para 0")
                    horas_extras = 0
                elif horas_extras > 0:
                    valor_he = horas_extras * (valor_hora * 2)
                    print(f"   [OK] {horas_extras:.1f}h × R$ {valor_hora * 2:.2f} = R$ {valor_he:.2f}")
            except ValueError:
                print("   [ERRO] Valor inválido! Considerando 0 horas extras.")
                horas_extras = 0
        else:
            # Cargos de confiança (gerente/diretor) não recebem hora extra
            print(f"\n   [INFO] {cargo} não recebe hora extra (cargo de confiança).")
        
        # ====================================================================
        # BLOCO FINALLY - SEMPRE EXECUTADO
        # ====================================================================
        # Chama a função pura que realiza todos os cálculos de folha
        resultado = processar_funcionario(nome, cargo, horas_extras)
        
        # Extrai os valores calculados para exibição
        salario_bruto = resultado['bruto']
        desconto_inss = resultado['inss']
        desconto_ir = resultado['ir']
        salario_liquido = resultado['liquido']
        valor_extras = resultado['extras']
        valor_hora = resultado['valor_hora']
        
        # Exibe os resultados calculados com layout profissional
        print("\n" + "-"*70)
        print("   CÁLCULO DA REMUNERAÇÃO")
        print("-"*70)
        
        salario_base = 160 * valor_hora
        print(f"   Salário Base (160h):        R$ {salario_base:>12.2f}")
        
        if valor_extras > 0:
            print(f"   Horas Extras (+100%):       R$ {valor_extras:>12.2f}")
        
        print(f"   {'─'*50}")
        print(f"   Salário Bruto:              R$ {salario_bruto:>12.2f}")
        print(f"\n   DESCONTOS:")
        print(f"   INSS:                      -R$ {desconto_inss:>12.2f}")
        print(f"   IR:                        -R$ {desconto_ir:>12.2f}")
        print(f"   {'─'*50}")
        print(f"   Salário Líquido:            R$ {salario_liquido:>12.2f}")
        print("-"*70)
        
        # Adiciona o funcionário à lista para exibir no relatório final
        lista_funcionarios.append(resultado)
        print("\n[SUCESSO] Funcionário cadastrado com sucesso!")
    
    # ========================================================================
    # PASSO 3: ORDENAR A LISTA POR NOME (ORDEM ALFABÉTICA)
    # ========================================================================
    # sort() organiza a lista in-place (altera a lista original)
    # key=lambda x: x['nome'] define que a ordenação será pelo campo 'nome'
    # lambda x: x['nome'] é uma função anônima que retorna o nome do funcionário
    lista_funcionarios.sort(key=lambda x: x['nome'])
    
    # ========================================================================
    # PASSO 4: EXIBIR RELATÓRIO COMPLETO DA FOLHA DE PAGAMENTO
    # ========================================================================
    print("\n" + "="*70)
    print("   FOLHA DE PAGAMENTO - RELATÓRIO COMPLETO")
    print("   (Ordenada Alfabeticamente)")
    print("="*70)
    
    # Variáveis acumuladoras para totalização
    total_bruto = 0
    total_inss = 0
    total_ir = 0
    total_liquido = 0
    total_horas_extras = 0
    total_valor_extras = 0
    
    # Exibir dados detalhados de cada funcionário
    # enumerate(lista, 1) começa a contagem do 1 em vez de 0
    for i, f in enumerate(lista_funcionarios, 1):
        print(f"\n┌─ {i}. {f['nome'].upper()} " + "─"*(65 - len(f['nome'])))
        print(f"│  Cargo: {f['cargo']}")
        print(f"│  Valor/hora: R$ {f['valor_hora']:.2f}")
        
        # Exibe horas extras apenas se houver - com destaque
        if f['horas_extras'] > 0:
            print(f"│  Horas Extras: {f['horas_extras']:.1f}h × R$ {f['valor_hora'] * 2:.2f} = R$ {f['extras']:.2f}")
            total_horas_extras += f['horas_extras']
            total_valor_extras += f['extras']
        
        # Exibe os valores financeiros alinhados
        print(f"│")
        print(f"│  Salário Bruto:              R$ {f['bruto']:>12.2f}")
        print(f"│  (-) INSS:                   R$ {f['inss']:>12.2f}")
        print(f"│  (-) IR:                     R$ {f['ir']:>12.2f}")
        print(f"│  {'─'*50}")
        print(f"│  Salário Líquido:            R$ {f['liquido']:>12.2f}")
        print("└" + "─"*68)
        
        # Acumula os totais para exibir no final
        total_bruto += f['bruto']
        total_inss += f['inss']
        total_ir += f['ir']
        total_liquido += f['liquido']
    
    # ========================================================================
    # PASSO 5: EXIBIR TOTALIZADORES (RESUMO GERAL)
    # ========================================================================
    print("\n" + "="*70)
    print("   RESUMO GERAL DA FOLHA DE PAGAMENTO")
    print("="*70)
    print(f"\n   Total de funcionários: {len(lista_funcionarios)}")
    
    if total_horas_extras > 0:
        print(f"   Total de Horas Extras: {total_horas_extras:.1f}h")
        print(f"   Valor Total de Horas Extras: R$ {total_valor_extras:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Formatação monetária brasileira
    print(f"\n   {'─'*65}")
    print(f"   Salário Bruto Total:          R$ {total_bruto:>15,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"   Total INSS:                  -R$ {total_inss:>15,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"   Total IR:                    -R$ {total_ir:>15,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"   {'═'*65}")
    print(f"   Total Líquido (a pagar):      R$ {total_liquido:>15,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print("="*70)
    
    # ========================================================================
    # PASSO 6: CALCULAR CUSTO TOTAL DA EMPRESA (INCLUINDO ENCARGOS)
    # ========================================================================
    # Encargos patronais: FGTS (8%), PIS (1%), INSS patronal (20%), etc.
    # Total aproximado: 27,65% sobre o salário bruto
    encargos = total_bruto * 0.2765
    custo_total_empresa = total_liquido + total_inss + total_ir + encargos
    
    print(f"\n   {'─'*65}")
    print(f"   CUSTO TOTAL PARA A EMPRESA:")
    print(f"   (Inclui encargos patronais: FGTS, INSS Patronal, PIS - 27,65%)")
    print(f"\n   Encargos Patronais:           R$ {encargos:>15,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"   {'─'*65}")
    print(f"   Custo Total da Folha:         R$ {custo_total_empresa:>15,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print("="*70)
    print("")


# ============================================================================
# FUNÇÃO AUXILIAR PARA TESTES (OPCIONAL)
# ============================================================================
# Este bloco só é executado se o arquivo for rodado diretamente
# (não quando é importado como módulo em outro arquivo)

if __name__ == "__main__":
    print("Testando o Módulo de RH...\n")
    calcular_folha_pagamento()
