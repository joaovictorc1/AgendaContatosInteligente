# test_structure.py
# Este é um script de teste mais simples que serve como um "checklist"
# para garantir que os arquivos principais do projeto estão presentes no diretório.

import os
import sys

def test_file_structure():
    """Verifica se os arquivos essenciais para a aplicação existem."""
    print("=== Teste de Estrutura de Arquivos do Projeto ===")
    
    # Lista de arquivos considerados essenciais para a aplicação funcionar.
    required_files = [
        'main.py',
        'database.py',
        'auth.py',
        'crud_contatos.py',
        'estruturas.py',
        '.env'  # Importante para a conexão com o banco
    ]
    
    all_found = True
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ Arquivo '{filename}' encontrado.")
        else:
            print(f"✗ Arquivo essencial '{filename}' NÃO encontrado.")
            all_found = False
            
    return all_found

def main():
    """Função principal que executa o teste de estrutura."""
    print("Iniciando verificação da estrutura de arquivos do projeto...")
    
    if test_file_structure():
        print("\n🎉 Status: OK! Todos os arquivos essenciais do projeto estão presentes.")
        return 0
    else:
        print("\n⚠️ Status: Atenção! Estão faltando arquivos importantes. O programa pode não funcionar.")
        print("   Verifique a lista acima e garanta que todos os arquivos estejam na mesma pasta.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
