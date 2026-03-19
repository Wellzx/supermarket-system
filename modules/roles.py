import os
from modules.database import connect

def criar_cargo(nome, salario_base):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_criar_cargo = "INSERT INTO roles (name, base_salary) VALUES (%s, %s)"
                valores = (nome, salario_base)
                cur.execute(cmd_criar_cargo, valores)
        print(f"Cargo {nome} criado!")
    except Exception as e:
            print(f"Erro: {e}")
            
            
def listar_cargo():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_listar_cargo = "SELECT * FROM roles"
                cur.execute(cmd_listar_cargo)
                cargos = cur.fetchall()
                if not cargos:
                    print("Nenhum cargo encontrado.")
                for cargo in cargos:
                    print(f"ID: {cargo[0]} NOME: {cargo[1]} SALARIO BASE: {cargo[2]}")
    except Exception as e:
        print(f"Error: {e}")
        
def atualizar_cargo(id, nome, salario_base):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_atualizar_cargo = "UPDATE roles SET name = %s, base_salary = %s WHERE id = %s"
                valores = (id, nome, salario_base)
                cur.execute(cmd_atualizar_cargo, valores)
        print("Cargo atualizado!")
    except Exception as e:
        print(f"Erro: {e}")
        
        
def deletar_cargo(id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cmd_deletar_cargo = "DELETE FROM roles WHERE id = %s"
                valores = (id,)
                cur.execute(cmd_deletar_cargo, valores)
        print(f"Cargo deletado!")
    except Exception as e:
        print(f"Erro: {e}")
        

def menu_cargo():
    while True:
        print("\n=== Cargo ===")
        print("1 - Listar cargo")
        print("2 - Criar cargo")
        print("3 - Atualizar cargo")
        print("4 - Deletar cargo")
        print("0 - Sair")
        
        option = input("\nEscolha a opção: ")
        os.system("clear")
        
        match option:
            case "1":
                listar_cargo()
            case "2":
                nome_cargo = input("Nome: ")
                salario_base_cargo = float(input("Salario base: "))
                criar_cargo(nome_cargo, salario_base_cargo)
            case "3":
                listar_cargo()
                id = int(input("ID: "))
                nome = input("Nome: ")
                salario_base = float(input("Salario base: "))
                atualizar_cargo(id, nome, salario_base)
            case "4":
                listar_cargo()
                id = int(input("ID: "))
                deletar_cargo(id)
            case "0":
                print("Voce saiu do sistema.")
                break
            case _:
                print("Opção inválida")