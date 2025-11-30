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
        
     # ====================================================================
        # PASSO 2.2: VERIFICAR SE O PRODUTO JÁ EXISTE (EVITAR DUPLICIDADE)
        # ====================================================================
        # Busca no banco de dados pelo código
        produto_existente = db_session.query(Produto).filter_by(codigo=codigo).first()
        
        if produto_existente:
            # PRODUTO JÁ EXISTE: Apenas soma a quantidade (fusão/atualização)
            produto_existente.quantidade += quantidade_nova
            db_session.commit() # Salva a alteração
            
            print(f"\n Produto '{produto_existente.nome}' já existe no estoque!")
            print(f"   Quantidade atualizada: {produto_existente.quantidade} unidades")
        
        # ====================================================================
        # PASSO 2.3: SE NÃO ACHOU, CADASTRAR NOVO PRODUTO
        # ====================================================================
        else:
            # Solicita os dados completos do novo produto
            print("\n Produto novo! Coletando informações adicionais...")
            
            data = input(" Data de fabricação (ex: 26/11/2025): ").strip()
            fornecedor = input(" Fornecedor: ").strip()
            local = input(" Local no armazém (ex: Corredor A, Prateleira 3): ").strip()
            
            try:
                valor = float(input(" Valor unitário (R$): "))
                
                if valor < 0:
                    print(" Valor não pode ser negativo! Usando R$ 0,00")
                    valor = 0.0
                    
            except ValueError:
                print(" Valor inválido! Usando R$ 0,00")
                valor = 0.0

            # ====================================================================
            # PASSO 2.4: CRIAR O OBJETO PRODUTO E PERSISTIR NO BANCO
            # ====================================================================
            try:
                produto = Produto(
                    codigo=codigo,
                    nome=nome,
                    quantidade=quantidade_nova,
                    valor=valor,
                    fornecedor=fornecedor,
                    local=local,
                    data_fabricacao=data,
                )

                db_session.add(produto)
                db_session.commit()

                print(f"\n Produto '{produto.nome}' cadastrado com sucesso! (codigo={produto.codigo})")
            except Exception as e:
                # Em caso de erro ao instanciar ou persistir, mostrar aviso e continuar
                print(f" Erro ao criar/persistir o produto: {e}")