# estoque_entrada.py
# -*- coding: utf-8 -*-
# estoque_entrada.py
# ============================================================================
# MÓDULO 1: ESTOQUE - ENTRADA DE PRODUTOS
# ============================================================================
# Este módulo é responsável por cadastrar novos produtos no estoque.
# Utiliza BANCO DE DADOS (SQLAlchemy) para armazenar os dados.
# 
# CONCEITOS DEMONSTRADOS:
# - Interação com Banco de Dados
# - Laços de repetição (for)
# - Estruturas condicionais (if/else)
# - Validação e tratamento de duplicidade
# ============================================================================

from database import Produto

# ============================================================================
# FUNÇÕES DE LÓGICA PURA (PARA API E CLI)
# ============================================================================

def registrar_entrada_produto(db_session, codigo, nome, quantidade, valor_unitario=0.0, data=None, fornecedor=None, local=None):
    """
    Registra a entrada de um produto no estoque (Lógica Pura).
    
    Retorna:
        tuple: (produto_objeto, is_novo_produto)
    """
    if not nome:
        raise ValueError("Nome do produto é obrigatório")
    if quantidade <= 0:
        raise ValueError("Quantidade deve ser maior que zero")
    
    # Verifica se o produto já existe pelo código
    produto = db_session.query(Produto).filter_by(codigo=codigo).first() # Busca por código único
    
    if produto:
        # Atualizar produto existente
        produto.quantidade += quantidade # Incrementa quantidade
        produto.valor_unitario = valor_unitario if valor_unitario > 0 else produto.valor_unitario # Atualiza valor se fornecido
        if data:
            produto.data_fabricacao = data
        if fornecedor:
            produto.fornecedor = fornecedor
        if local:
            produto.local = local
        
        db_session.commit()
        return (produto, False)
    else:
        # Criar novo produto
        novo_produto = Produto(
            codigo=codigo,
            nome=nome,
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            data_fabricacao=data or "",
            fornecedor=fornecedor or "",
            local_armazem=local or ""
        )
        
        db_session.add(novo_produto)
        db_session.commit()
        return (novo_produto, True)


# ============================================================================
# FUNÇÕES INTERATIVAS (CLI)
# ============================================================================

def cadastrar_produtos(db_session):
    """
    Cadastra múltiplos produtos no estoque (Interface Console).
    """
    print("\n" + "="*70)
    print("   MÓDULO DE ESTOQUE - ENTRADA DE PRODUTOS")
    print("="*70)
    
    try:
        qtd_produtos = int(input("\nQuantos produtos deseja cadastrar? "))
        if qtd_produtos > 10:
            print("\n[AVISO] Limitado a 10 produtos conforme regra do sistema.")
            qtd_produtos = 10
        if qtd_produtos <= 0:
            print("\n[ERRO] Quantidade deve ser maior que zero!")
            return
    except ValueError:
        print("\n[ERRO] Digite apenas números inteiros!")
        return
    
    produtos_novos = 0
    produtos_atualizados = 0
    
    for i in range(qtd_produtos):
        print("\n" + "═"*70)
        print(f"   PRODUTO {i+1} DE {qtd_produtos}")
        print("═"*70)
        
        codigo = input("\nCódigo do produto: ").strip()
        if not codigo:
            print("[ERRO] Código não pode estar vazio! Pulando este produto.")
            continue
        
        nome = input("Nome do produto: ").strip()
        if not nome:
            print("[ERRO] Nome não pode estar vazio! Pulando este produto.")
            continue
        
        try:
            quantidade = int(input("Quantidade: "))
            if quantidade <= 0:
                print("[ERRO] Quantidade deve ser maior que zero! Pulando este produto.")
                continue
        except ValueError:
            print("[ERRO] Quantidade inválida! Pulando este produto.")
            continue
        
        try:
            valor = float(input("Valor unitário (R$): "))
            if valor < 0:
                print("[AVISO] Valor negativo ajustado para R$ 0.00")
                valor = 0.0
        except ValueError:
            print("[AVISO] Valor inválido, será definido como R$ 0.00")
            valor = 0.0
        
        data = input("Data de fabricação (opcional): ").strip()
        fornecedor = input("Fornecedor (opcional): ").strip()
        local = input("Local de armazenamento (opcional): ").strip()
        
        # Chama a função pura
        try:
            produto, is_novo = registrar_entrada_produto(
                db_session, codigo, nome, quantidade, valor_unitario=valor, data=data, fornecedor=fornecedor, local=local
            )
            
            valor_total = quantidade * valor
            
            if is_novo:
                print("\n" + "─"*70)
                print("[SUCESSO] PRODUTO CADASTRADO!")
                print("─"*70)
                print(f"   Código: {produto.codigo}")
                print(f"   Nome: {produto.nome}")
                print(f"   Quantidade: {produto.quantidade} unidades")
                print(f"   Valor Unitário: R$ {produto.valor_unitario:.2f}")
                print(f"   Valor Total: R$ {valor_total:.2f}")
                if fornecedor:
                    print(f"   Fornecedor: {produto.fornecedor}")
                if local:
                    print(f"   Local: {produto.local_armazem}")
                print("─"*70)
                produtos_novos += 1
            else:
                print("\n" + "─"*70)
                print("[SUCESSO] PRODUTO ATUALIZADO!")
                print("─"*70)
                print(f"   Nome: {produto.nome}")
                print(f"   Quantidade Anterior: {produto.quantidade - quantidade} unidades")
                print(f"   Quantidade Adicionada: {quantidade} unidades")
                print(f"   Nova Quantidade Total: {produto.quantidade} unidades")
                print(f"   Valor Unitário: R$ {produto.valor_unitario:.2f}")
                print("─"*70)
                produtos_atualizados += 1
                
        except Exception as e:
            print(f"\n[ERRO] Erro ao cadastrar produto: {e}")
    
    print("\n" + "═"*70)
    print("   RESUMO DO CADASTRO")
    print("═"*70)
    print(f"   Produtos novos cadastrados: {produtos_novos}")
    print(f"   Produtos atualizados: {produtos_atualizados}")
    print(f"   Total processado: {produtos_novos + produtos_atualizados}")
    print("═"*70)


# Alias para manter compatibilidade com main.py
cadastrar_produto = cadastrar_produtos


if __name__ == "__main__":
    print(" Testando o Módulo de Entrada de Estoque...\n")
