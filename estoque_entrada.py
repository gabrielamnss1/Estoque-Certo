from src.database import Produto

def cadastrar_produto(db_session):
    
    print("\n" + "="*50)
    print("   MÓDULO 2: ENTRADA DE ESTOQUE")
    print("="*50)
    
    # ========================================================================
    # PASSO 1: DEFINIR QUANTOS PRODUTOS SERÃO CADASTRADOS
    # ========================================================================
    try:
        qtd_cadastro = int(input("\n Quantos produtos deseja cadastrar agora? "))

        if qtd_cadastro <= 0:
            print("\n Quantidade deve ser maior que zero!")
            return

    except ValueError:
        print("\n Erro: Digite apenas números inteiros!")
        return
    
    # ========================================================================
    # PASSO 2: LOOP PARA CADASTRAR CADA PRODUTO
    # ========================================================================
    
    for i in range(qtd_cadastro):
        print("\n" + "-"*50)
        print(f" CADASTRANDO PRODUTO {i+1} DE {qtd_cadastro}")
        print("-"*50)
        
        # ====================================================================
        # PASSO 2.1: COLETAR DADOS BÁSICOS (CÓDIGO, NOME, QUANTIDADE)
        # ====================================================================
        
        try:
            codigo = int(input(" Código do produto: "))
            nome = input(" Nome do produto: ").strip()
            
            if not nome:
                print(" Nome não pode estar vazio! Pulando este produto.")
                continue
                
            quantidade_nova = int(input(" Quantidade: "))
            
            if quantidade_nova <= 0:
                print(" Quantidade deve ser maior que zero! Pulando este produto.")
                continue
                
        except ValueError:
            print(" Erro: Dados inválidos! Pulando este produto.")
            continue