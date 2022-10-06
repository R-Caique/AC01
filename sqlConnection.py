import pyodbc
from contextlib import closing

dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-QBR6RNK;"
    "Database=Nargas_Delivery;"
)

sql_structure = """
    create table Clientes(
        id_cliente int primary key identity(1,1),
        nome varchar(150) not null,
        sexo varchar(10) not null,
        telefone varchar(20) not null,
        cep varchar(15) not null,
        pais varchar(50) not null,
        estado varchar(50) not null,
        municipio varchar(50) not null,
        rua varchar(150) not null,
        numero int not null,
    )

    create table Acessos(
        id_acesso int primary key identity(1,1),
        id_conta varchar(50) not null,
        email varchar(150) not null,
        senha varchar(30) not null,
    )

    create table Categorias(
        id_categoria int primary key identity(1,1),
        nome varchar(150) not null,
        descrição varchar(255) not null,
    )

    create table Produtos(
        id_produto int primary key identity(1,1),
        nome varchar(150) not null,
        descricao varchar(255) not null,
        quantidade int not null,
        id_categoria int foreign key references categorias(id_categoria)
    )
"""

def conectar():
    return  pyodbc.connect(dados_conexao)

def sqlSv_create_structure():
    with closing(conectar()) as conn, closing(conn.cursor()) as cur:
        cur.execute(sql_structure)
        cur.commit()

# sqlSv_create_structure()

def sqlSv_addAccess(id_conta, email, senha):
    query_addAccess = f"INSERT INTO Acessos VALUES ('{id_conta}', '{email}', '{senha}')"
    with closing(conectar()) as conn, closing(conn.cursor()) as cur:
        cur.execute(query_addAccess)
        cur.commit()

        return {
            'id_conta': id_conta,
            'email': email,
            'senha': senha,
        }

def sqlSv_access(login, senha):
    query_login = f"SELECT id_conta, senha FROM Acessos WHERE id_conta = '{login}' AND senha = '{senha}'"
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute(query_login)
        return row_to_dict(cur.description, cur.fetchone())

# Converte uma linha em um dicionário.
def row_to_dict(description, row):
    if row is None: return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result
