import os
from modules.database import connect

def criar_fornecedor(nome, telefone, email):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_criar_fornecedor = "INSERT INTO suppliers (name, phone, email) VALUES (%s, %s, %s)"
                valores = (nome, telefone, email)
                cur.execute(cmd_criar_fornecedor, valores)
        print(f"Fornecedor {nome} criado!")
    except Exception as e:
            print(f"Erro: {e}")
            
def listar_fornecedor():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_listar_fornecedor = "SELECT * FROM suppliers"
                cur.execute(cmd_listar_fornecedor)
                fornecedores = cur.fetchall()
                if not fornecedores:
                    print("Nenhum fornecedor encontrado.")
                for fornecedor in fornecedores:
                    print(f"ID: {fornecedor[0]} Nome: {fornecedor[1]} Telefone: {fornecedor[2]} Email: {fornecedor[3]}")
    except Exception as e:
        print(f"Error: {e}")
        
def atualizar_fornecedor(id, nome, telefone, email):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_atualizar_fornecedor = "UPDATE suppliers SET name = %s, phone = %s, email = %s WHERE id = %s"
                valores = (nome, telefone, email, id)
                cur.execute(cmd_atualizar_fornecedor, valores)
        print("Fornecedor atualizado!")
    except Exception as e:
        print(f"Erro: {e}")
        
def deletar_fornecedor(id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_deletar_fornecedor = "DELETE FROM suppliers WHERE id = %s"
                valores = (id,)
                cur.execute(cmd_deletar_fornecedor, valores)
        print(f"Fornecedor deletado!")
    except Exception as e:
        print(f"Erro: {e}")
        
def menu_fornecedor():
    while True:
        print("\n=== Fornecedores ===")
        print("1 - Listar fornecedor")
        print("2 - Criar fornecedor")
        print("3 - Atualizar fornecedor")
        print("4 - Deletar fornecedor")
        print("0 - Sair")
        
        option = input("\nEscolha a opção: ")
        os.system("clear")
        
        match option:
            case "1":
                listar_fornecedor()
            case "2":
                nome_fornecedor = input("Nome: ")
                telefone_fornecedor = input("Telefone: ").strip() or None
                email_fornecedor = input("Email: ").strip() or None
                criar_fornecedor(nome_fornecedor, telefone_fornecedor, email_fornecedor)
            case "3":
                listar_fornecedor()
                id = int(input("ID: "))
                nome = input("Nome: ")
                telefone = input("Telefone: ").strip() or None
                email = input("Email: ").strip() or None
                atualizar_fornecedor(id, nome, telefone, email)
            case "4":
                listar_fornecedor()
                id = int(input("ID: "))
                deletar_fornecedor(id)
            case "0":
                print("Voce saiu do sistema.")
                break
            case _:
                print("Opção inválida")