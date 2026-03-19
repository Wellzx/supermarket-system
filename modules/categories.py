import os
from modules.database import connect

def criar_categoria(nome):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_criar_categoria = "INSERT INTO categories (name) VALUES (%s)"
                valores = (nome,)
                cur.execute(cmd_criar_categoria, valores)
        print(f"Categoria {nome} criada!")
    except Exception as e:
        print(f"Erro: {e}")
        
        
def listar_categorias():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_listar_categorias = "SELECT * FROM categories"
                cur.execute(cmd_listar_categorias)
                categorias = cur.fetchall()
                if not categorias:
                    print("Nenhuma categoria encontrada.")
                for categoria in categorias:
                    print(f"ID: {categoria[0]} NOME: {categoria[1]}")
    except Exception as e:
        print(f"Erro: {e}")
        
def atualizar_categoria(id, nome):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_atualizar_categoria = "UPDATE categories SET name = %s WHERE id = %s"
                valores = (nome, id)
                cur.execute(cmd_atualizar_categoria, valores)
        print("Categoria atualizada!")
    except Exception as e:
        print(f"Erro: {e}")
        
def deletar_categoria(id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_deletar_categoria = "DELETE FROM categories WHERE id = %s"
                valores = (id,)
                cur.execute(cmd_deletar_categoria, valores)
        print(f"Categoria deletada!")
    except Exception as e:
        print(f"Erro: {e}")
        
def menu_categorias():
    while True:
        print("\n=== Categorias ===")
        print("1 - Listar categoria")
        print("2 - Criar categoria")
        print("3 - Atualizar categoria")
        print("4 - Deletar categoria")
        print("0 - Sair")
        
        option = input("\nEscolha a opção: ")
        os.system("clear")
        
        match option:
            case "1":
                listar_categorias()
            case "2":
                nome_categoria = input("Nome: ")
                criar_categoria(nome_categoria)
            case "3":
                listar_categorias()
                id = int(input("ID: "))
                nome = input("Nome: ")
                atualizar_categoria(id, nome)
            case "4":
                listar_categorias()
                id = int(input("ID: "))
                deletar_categoria(id)
            case "0":
                print("Voce saiu do sistema.")
                break
            case _:
                print("Opção inválida")
                