# Sistema Quatro Cantos

Sistema de Gestão Empresarial desenvolvido em Python com módulos integrados para operações, estoque, finanças e recursos humanos.

## Visão Geral

O Sistema Quatro Cantos é uma solução completa para gestão empresarial que oferece:

- **Módulo Operacional**: Cálculo de capacidade produtiva por turnos
- **Gestão de Estoque**: Controle de entrada e saída de produtos
- **Módulo Financeiro**: Análise de custos, precificação e projeções
- **Recursos Humanos**: Folha de pagamento com INSS e IR progressivos

## Instalação Rápida

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/gabrielamnss1/Quatro-Cantos.git
cd Quatro-Cantos
```

2. **Crie e ative o ambiente virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**

```bash
pip install sqlalchemy python-dotenv bcrypt
```

4. **Execute o sistema**

```bash
python main.py
```

## Estrutura do Projeto

```
Quatro-Cantos/
│
├── src/
│   ├── main.py                 # Arquivo principal e menu
│   ├── database.py             # Configuração do banco e modelos
│   ├── auth_utils.py           # Utilitários de autenticação
│   ├── operacional.py          # Módulo operacional
│   ├── estoque_entrada.py      # Entrada de produtos
│   ├── estoque_saida.py        # Saída de produtos
│   ├── financeiro.py           # Módulo financeiro
│   └── rh.py                   # Recursos humanos
│
├── docs/
│   ├── index.html              # Documentação completa
│   └── fluxograma.html         # Fluxograma interativo do sistema
│
├── .env                        # Configurações (não versionado)
├── .gitignore                  # Arquivos ignorados
└── README.md                   # Este arquivo
```

## Módulos do Sistema

### 1. Módulo Operacional

Calcula a capacidade de produção da fábrica baseada em turnos:

- Capacidade por turno: 1.666 unidades
- Cálculo de projeções diárias, mensais e anuais
- Análise de ociosidade e percentual de uso

### 2. Gestão de Estoque

**Entrada de Produtos:**
- Cadastro de produtos com nome, quantidade e preço
- Validação de dados e integração com banco

**Saída de Produtos:**
- Registro de vendas e saídas
- Verificação de disponibilidade de estoque
- Atualização automática das quantidades

### 3. Módulo Financeiro

- Cadastro de custos operacionais (água, luz, impostos, folha)
- Cálculo de custo por unidade
- Precificação com margem de lucro (50%)
- Indicadores: ROI, ponto de equilíbrio
- Projeções mensais e anuais de receita e lucro

### 4. Recursos Humanos

- Hierarquia de cargos: Operário, Supervisor, Gerente, Diretor
- Cálculo de horas extras (valor dobrado)
- INSS progressivo (tabela 2025)
- Imposto de Renda progressivo (tabela 2025)
- Relatório completo da folha de pagamento

## Configuração

### Banco de Dados

Por padrão, o sistema usa SQLite (arquivo local). Para usar PostgreSQL:

1. Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://usuario:senha@localhost/nome_banco
```

2. O sistema detectará automaticamente e usará PostgreSQL

### Variáveis de Ambiente

```env
# Banco de dados
DATABASE_URL=sqlite:///dados.db

# Para PostgreSQL
# DATABASE_URL=postgresql://usuario:senha@localhost:5432/banco

# Para MySQL
# DATABASE_URL=mysql://usuario:senha@localhost:3306/banco
```

## Uso

1. Execute `python main.py`
2. Escolha um módulo digitando o número correspondente
3. Siga as instruções na tela
4. Visualize os resultados
5. Pressione Enter para retornar ao menu

### Exemplo: Calcular Capacidade Produtiva

```
python main.py
> Digite: 1
> Quantos turnos estarão ativos (1, 2 ou 3)? 2

Resultado:
- Capacidade diária: 3.332 unidades
- Capacidade mensal: 99.960 unidades  
- Capacidade anual: 1.199.520 unidades
- Percentual de uso: 66,67%
```

## Tecnologias

- **Python 3.x**: Linguagem principal
- **SQLAlchemy**: ORM para banco de dados
- **SQLite/PostgreSQL**: Banco de dados
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **bcrypt**: Hash seguro de senhas

## Conceitos de Programação

O sistema demonstra diversos conceitos importantes:

- Programação Orientada a Objetos (POO)
- Funções puras e separação de lógica
- Validação e tratamento de exceções
- Estruturas condicionais e de repetição
- Manipulação de coleções (listas e dicionários)
- ORM (Object-Relational Mapping)
- Cálculos progressivos (impostos por faixa)
- Formatação de dados e relatórios

## Documentação Completa

Para documentação detalhada com todos os recursos, exemplos e guias passo a passo, 
acesse a documentação HTML completa:

```bash
# Abra no navegador
docs/index.html
```

A documentação inclui:
- Guia completo de instalação
- Descrição detalhada de cada módulo
- Estrutura do banco de dados
- Exemplos práticos de uso
- Tabelas de INSS e IR atualizadas
- Conceitos de programação aplicados
- Arquitetura do sistema
- Práticas de segurança

## Segurança

- Senhas são armazenadas com hash bcrypt
- Validação de todas as entradas do usuário
- Configurações sensíveis em arquivo .env (não versionado)
- Proteção contra SQL injection via ORM

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Suporte

- **Issues**: https://github.com/gabrielamnss1/Quatro-Cantos/issues
- **Documentação HTML**: Abra `docs/index.html` no navegador
- **Fluxograma**: Abra `docs/fluxograma.html` no navegador

## Licença

Este projeto foi desenvolvido para fins educacionais e de gestão empresarial.

## Autores

Sistema desenvolvido pela equipe Quatro Cantos.

---
Equipe
Informações do Projeto
Disciplina: Lógica de Programação
Professor: Washington Luis Souza Anunciação
Data de Início: 22 de novembro de 2025
Integrantes
#	Nome Completo	Email
1	Gabriela M. N. Silva	gabriela.m.silva@ba.estudante.senai.br
2	Cristiano Silva Santos	Cristiano.s.santos@ba.estudante.senai.br
3	Joel Macena Costa	joel.c@ba.estudante.senai.br

Gabriela M. N. Silva (gabriela.m.silva@ba.estudante.senai.br): Desenvolvedora principal, autora da conta GitHub, integração com repositório remoto
Cristiano Silva Santos (Cristiano.s.santos@ba.estudante.senai.br): Desenvolvedor, contribuidor do projeto
Joel Macena Costa (joel.c@ba.estudante.senai.br): Desenvolvedor, contribuidor do projeto

Contribuições
Todos os integrantes contribuem para:

Implementação de funcionalidades
Testes e validação
Documentação
Revisão de código

**Versão**: 1.0  
**Última atualização**: Dezembro 2025
