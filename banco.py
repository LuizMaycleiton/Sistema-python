import sqlite3

def conectar_banco():
    conexao = sqlite3.connect("atelier_bolo.db", check_same_thread=False)
    cursor = conexao.cursor()

    # 1. Tabela de Clientes
    sql_clientes = '''
    create table if not exists clientes (
        id integer primary key autoincrement,
        nome text not null,
        telefone text not null,
        endereco text not null
    )
    '''
    cursor.execute(sql_clientes)

    # 2. Tabela de Produtos Prontos & Bebidas
    sql_produtos = '''
    create table if not exists produtos (
        id integer primary key autoincrement,
        nome text not null,
        categoria text not null,
        preco real not null
    )
    '''
    cursor.execute(sql_produtos)

    # 3. Tabela de Massas e Recheios
    sql_opcoes = '''
    create table if not exists opcoes_bolo (
        id integer primary key autoincrement,
        tipo text not null,
        nome text not null
    )
    '''
    cursor.execute(sql_opcoes)

    # 4. Tabela de Preço por Kg
    sql_config = '''
    create table if not exists configuracoes (
        chave text primary key,
        valor real not null
    )
    '''
    cursor.execute(sql_config)

    # 5. Tabela de Motoboys
    sql_motoboys = '''
    create table if not exists motoboys (
        id integer primary key autoincrement,
        nome text not null,
        telefone text not null,
        placa text not null,
        tipo_bau text not null,
        status text not null
    )
    '''
    cursor.execute(sql_motoboys)

    # 6. Tabela de Pedidos
    sql_pedidos = '''
    create table if not exists pedidos (
        id integer primary key autoincrement,
        cliente_id integer not null,
        motoboy_id integer,
        descricao_itens text not null,
        peso_bolo real not null,
        taxa_entrega real not null,
        valor_total real not null,
        etapa text not null,
        data_pedido text default (datetime('now', 'localtime'))
    )
    '''
  