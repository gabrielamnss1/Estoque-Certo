# ============================================================================
# MÓDULO AUTH_UTILS - UTILITÁRIOS DE AUTENTICAÇÁO SEGURA
# ============================================================================
# Este módulo fornece funções para hash e verificação de senhas usando bcrypt
# 
# SEGURANÇA:
# - Bcrypt é um algoritmo de hashing projetado para senhas
# - Utiliza salt automático para prevenir ataques rainbow table
# - Computacionalmente caro (dificulta ataques de força bruta)
# ============================================================================

import bcrypt

def hash_password(password: str) -> str:
    """
    Gera um hash seguro da senha usando bcrypt.
    
    Args:
        password: Senha em texto claro
        
    Returns:
        Hash da senha como string (pode ser armazenado no banco)
        
    Example:
        >>> hashed = hash_password("minha_senha_123")
        >>> print(hashed)
        '$2b$12$...'
    """
    # Converte a senha para bytes
    password_bytes = password.encode('utf-8')
    
    # Gera o salt e cria o hash
    # rounds=12 é um bom balanço entre segurança e performance
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Retorna como string para armazenamento
    return hashed.decode('utf-8')

