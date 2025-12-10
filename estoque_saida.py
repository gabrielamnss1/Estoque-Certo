# -*- coding: utf-8 -*-
# estoque_saida.py
# ============================================================================
# MÓDULO 2: ESTOQUE - SAÍDA DE PRODUTOS (VENDAS)
# ============================================================================
# Este módulo é responsável por registrar vendas e dar baixa no estoque.
# Implementa lógica de busca e verificação de saldo disponível.
#
# CONCEITOS DEMONSTRADOS:
# - Interação com Banco de Dados (SQLAlchemy)
# - Busca case-insensitive no banco
# - Estruturas condicionais complexas (if/elif/else)
# - Atualização de dados no banco
# - Validação de estoque
# - Tratamento de pedidos parciais
# ============================================================================

from database import Produto
from sqlalchemy import func

# ============================================================================
# FUNÇÕES DE LÓGICA PURA (PARA API E CLI)
# ============================================================================

def registrar_saida_produto(db_session, nome_buscado, qtd_desejada):
    """
    Registra a saída de um produto do estoque (Lógica Pura).

    Retorna:
        dict: Resultado da operação com status, tipo de atendimento, valores, etc.
    """
    if not nome_buscado:
        raise ValueError("Nome do produto é obrigatório")
    if qtd_desejada <= 0:
        raise ValueError("Quantidade deve ser maior que zero")

    # Busca case-insensitive
    produto = db_session.query(Produto).filter(func.lower(Produto.nome) == nome_buscado.lower()).first()

    if not produto:
        return {
            "status": "erro",
            "mensagem": "Produto não encontrado",
            "produto": None
        }

    saldo_atual = produto.quantidade
    valor_unitario = produto.valor_unitario

    resultado = {
        "produto": produto,
        "saldo_anterior": saldo_atual,
        "valor_unitario": valor_unitario,
        "qtd_solicitada": qtd_desejada
    }

    if saldo_atual >= qtd_desejada:
        # Atendimento Completo
        produto.quantidade -= qtd_desejada
        valor_venda = qtd_desejada * valor_unitario

        resultado.update({
            "status": "sucesso",
            "tipo": "completo",
            "qtd_vendida": qtd_desejada,
            "valor_venda": valor_venda,
            "saldo_restante": produto.quantidade
        })

    elif saldo_atual > 0:
        # Atendimento Parcial
        valor_venda = saldo_atual * valor_unitario
        produto.quantidade = 0

        resultado.update({
            "status": "parcial",
            "tipo": "parcial",
            "qtd_vendida": saldo_atual,
            "valor_venda": valor_venda,
            "saldo_restante": 0
        })

    else:
        # Esgotado
        resultado.update({
            "status": "erro",
            "mensagem": "Produto esgotado",
            "tipo": "esgotado",
            "qtd_vendida": 0,
            "valor_venda": 0.0,
            "saldo_restante": 0
        })
        return resultado

    if resultado["status"] in ["sucesso", "parcial"]:
        db_session.commit()

    return resultado


# ============================================================================
# FUNÇÕES INTERATIVAS (CLI)
# ============================================================================

def vender_produto(db_session):
    """
    Registra vendas/saídas de produtos do estoque (Interface Console).
    """
    print("\n" + "="*70)
    print("   MÓDULO DE ESTOQUE - SAÍDA DE PRODUTOS (VENDAS)")
    print("="*70)
    
    # Listar produtos disponíveis
    print("\nPRODUTOS DISPONÍVEIS EM ESTOQUE:")
    print("─"*70)
    
    produtos = db_session.query(Produto).filter(Produto.quantidade > 0).all()
    
    if not produtos:
        print("\n[AVISO] Nenhum produto disponível em estoque!")
        print("   Cadastre produtos primeiro no Módulo de Entrada.")
        return
    
    for i, p in enumerate(produtos, 1):
        valor_estoque = p.quantidade * p.valor_unitario
        print(f"{i}. {p.nome}")
        print(f"   Código: {p.codigo} | Qtd: {p.quantidade} un | R$ {p.valor_unitario:.2f}/un | Total: R$ {valor_estoque:.2f}")
    
    print("─"*70)
    
    # Continuar vendendo
    total_vendas = 0.0
    qtd_vendas = 0
    
    while True:
        print("\n" + "═"*70)
        nome_produto = input("\nDigite o nome do produto (ou 'sair' para finalizar): ").strip()
        
        if nome_produto.lower() == 'sair':
            break
        
        if not nome_produto:
            print("[ERRO] Nome não pode estar vazio!")
            continue
        
        try:
            qtd_desejada = int(input("Quantidade desejada: "))
            if qtd_desejada <= 0:
                print("[ERRO] Quantidade deve ser maior que zero!")
                continue
        except ValueError:
            print("[ERRO] Digite apenas números inteiros!")
            continue
        
        # Chama a função pura
        try:
            resultado = registrar_saida_produto(db_session, nome_produto, qtd_desejada)
            
            print("\n" + "─"*70)
            
            if resultado["status"] == "sucesso":
                print("[SUCESSO] VENDA REALIZADA COM SUCESSO!")
                print("─"*70)
                print(f"   Produto: {resultado['produto'].nome}")
                print(f"   Quantidade Vendida: {resultado['qtd_vendida']} unidades")
                print(f"   Valor Unitário: R$ {resultado['valor_unitario']:.2f}")
                print(f"   Valor Total da Venda: R$ {resultado['valor_venda']:.2f}")
                print(f"   Saldo Anterior: {resultado['saldo_anterior']} unidades")
                print(f"   Saldo Atual: {resultado['saldo_restante']} unidades")
                print("─"*70)
                total_vendas += resultado['valor_venda']
                qtd_vendas += 1
                
            elif resultado["status"] == "parcial":
                print("[AVISO] ATENDIMENTO PARCIAL")
                print("─"*70)
                print(f"   Produto: {resultado['produto'].nome}")
                print(f"   Quantidade Solicitada: {resultado['qtd_solicitada']} unidades")
                print(f"   Quantidade Disponível: {resultado['saldo_anterior']} unidades")
                print(f"   Quantidade Vendida: {resultado['qtd_vendida']} unidades")
                print(f"   Valor Unitário: R$ {resultado['valor_unitario']:.2f}")
                print(f"   Valor Total da Venda: R$ {resultado['valor_venda']:.2f}")
                print(f"   [AVISO] Saldo Insuficiente! Produto agora está ESGOTADO.")
                print("─"*70)
                total_vendas += resultado['valor_venda']
                qtd_vendas += 1
                
            else:  # erro
                print("[ERRO] ERRO NA VENDA")
                print("─"*70)
                print(f"   {resultado.get('mensagem', 'Erro desconhecido')}")
                if resultado.get('tipo') == 'esgotado':
                    print(f"   Produto '{nome_produto}' está sem estoque!")
                print("─"*70)
                
        except Exception as e:
            print(f"\n[ERRO] Erro ao processar venda: {e}")
        
        # Perguntar se deseja continuar
        continuar = input("\n>> Registrar outra venda? (s/n): ").strip().lower()
        if continuar != 's':
            break
    
    # Resumo final
    if qtd_vendas > 0:
        print("\n" + "═"*70)
        print("   RESUMO DAS VENDAS")
        print("═"*70)
        print(f"   Quantidade de Vendas: {qtd_vendas}")
        print(f"   Faturamento Total: R$ {total_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print("═"*70)
    else:
        print("\n[AVISO] Nenhuma venda foi registrada.")


if __name__ == "__main__":
    print("Testando o Módulo de Saída de Estoque...\n")
