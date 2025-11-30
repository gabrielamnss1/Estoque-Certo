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
