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
  
   # --- DADOS INICIAIS DE TESTE ---
   
    cursor.execute("select count(*) from configuracoes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("insert into configuracoes (chave, valor) values ('preco_kg', 60.00)")

    cursor.execute("select count(*) from motoboys")
    if cursor.fetchone()[0] == 0:
        cursor.execute("insert into motoboys (nome, telefone, placa, tipo_bau, status) values ('Roberto Alves', '(11) 98888-7777', 'ABC-1234', 'Baú Plano Grande', 'Disponível')")
        cursor.execute("insert into motoboys (nome, telefone, placa, tipo_bau, status) values ('Thiago Souza', '(11) 97777-6666', 'XYZ-5678', 'Baú Padrão', 'Disponível')")

    cursor.execute("select count(*) from produtos")
    if cursor.fetchone()[0] == 0:
        cursor.execute("insert into produtos (nome, categoria, preco) values ('Bolo Médio de Cenoura', 'Bolo Médio', 45.00)")
        cursor.execute("insert into produtos (nome, categoria, preco) values ('Fatia Red Velvet', 'Fatia', 14.00)")
        cursor.execute("insert into produtos (nome, categoria, preco) values ('Coca-Cola 2L', 'Bebida', 12.00)")

    cursor.execute("select count(*) from opcoes_bolo")
    if cursor.fetchone()[0] == 0:
        cursor.execute("insert into opcoes_bolo (tipo, nome) values ('Massa', 'Branca')")
        cursor.execute("insert into opcoes_bolo (tipo, nome) values ('Massa', 'Chocolate')")
        cursor.execute("insert into opcoes_bolo (tipo, nome) values ('Recheio', 'Ninho com Morango')")
        cursor.execute("insert into opcoes_bolo (tipo, nome) values ('Recheio', 'Brigadeiro')")

    cursor.execute("select count(*) from clientes")
    if cursor.fetchone()[0] == 0:
        cursor.execute("insert into clientes (nome, telefone, endereco) values ('João Pedro', '(11) 99999-0000', 'Rua das Acácias, 120')")
        cursor.execute("insert into clientes (nome, telefone, endereco) values ('Carla Dias', '(11) 98888-8888', 'Rua das Flores, 45')")

    conexao.commit()
    return conexao, cursor


# CLIENTES

def cadastrar_cliente(nome, telefone, endereco):
    conexao, cursor = conectar_banco()
    sql = '''
    insert into clientes (nome, telefone, endereco)
    values (?, ?, ?)
    '''
    cursor.execute(sql, (nome, telefone, endereco))
    conexao.commit()


def listar_clientes():
    conexao, cursor = conectar_banco()
    sql = '''
    select * from clientes
    '''
    cursor.execute(sql)
    resultados = cursor.fetchall()
    return resultados


# PRODUTOS E OPÇÕES DE BOLO

def cadastrar_produto(nome, categoria, preco):
    conexao, cursor = conectar_banco()
    sql = '''
    insert into produtos (nome, categoria, preco)
    values (?, ?, ?)
    '''
    cursor.execute(sql, (nome, categoria, preco))
    conexao.commit()


def listar_produtos():
    conexao, cursor = conectar_banco()
    sql = '''
    select * from produtos
    '''
    cursor.execute(sql)
    resultados = cursor.fetchall()
    return resultados


def excluir_produto(id_produto):
    conexao, cursor = conectar_banco()
    sql = '''
    delete from produtos where id = ?
    '''
    cursor.execute(sql, (id_produto,))
    conexao.commit()


def cadastrar_opcao_bolo(tipo, nome):
    conexao, cursor = conectar_banco()
    sql = '''
    insert into opcoes_bolo (tipo, nome)
    values (?, ?)
    '''
    cursor.execute(sql, (tipo, nome))
    conexao.commit()


def listar_opcoes_bolo():
    conexao, cursor = conectar_banco()
    sql = '''
    select * from opcoes_bolo
    '''
    cursor.execute(sql)
    resultados = cursor.fetchall()
    return resultados


def listar_opcoes_por_tipo(tipo):
    conexao, cursor = conectar_banco()
    sql = '''
    select * from opcoes_bolo where tipo = ?
    '''
    cursor.execute(sql, (tipo,))
    resultados = cursor.fetchall()
    return resultados


def excluir_opcao_bolo(id_opcao):
    conexao, cursor = conectar_banco()
    sql = '''
    delete from opcoes_bolo where id = ?
    '''
    cursor.execute(sql, (id_opcao,))
    conexao.commit()


def obter_preco_kg():
    conexao, cursor = conectar_banco()
    sql = '''
    select valor from configuracoes where chave = 'preco_kg'
    '''
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado[0]


def atualizar_preco_kg(novo_valor):
    conexao, cursor = conectar_banco()
    sql = '''
    update configuracoes set valor = ? where chave = 'preco_kg'
    '''
    cursor.execute(sql, (novo_valor,))
    conexao.commit()


# MOTOBOYS

def cadastrar_motoboy(nome, telefone, placa, tipo_bau):
    conexao, cursor = conectar_banco()
    sql = '''
    insert into motoboys (nome, telefone, placa, tipo_bau, status)
    values (?, ?, ?, ?, 'Disponível')
    '''
    cursor.execute(sql, (nome, telefone, placa, tipo_bau))
    conexao.commit()


def listar_motoboys():
    conexao, cursor = conectar_banco()
    sql = '''
    select * from motoboys
    '''
    cursor.execute(sql)
    resultados = cursor.fetchall()
    return resultados


def listar_motoboys_disponiveis(peso_bolo):
    conexao, cursor = conectar_banco()
    if peso_bolo > 2.0:
        sql = '''
        select * from motoboys where status = 'Disponível' and tipo_bau = 'Baú Plano Grande'
        '''
    else:
        sql = '''
        select * from motoboys where status = 'Disponível'
        '''
    cursor.execute(sql)
    resultados = cursor.fetchall()
    return resultados


def alterar_status_motoboy(id_motoboy, novo_status):
    conexao, cursor = conectar_banco()
    sql = '''
    update motoboys set status = ? where id = ?
    '''
    cursor.execute(sql, (novo_status, id_motoboy))
    conexao.commit()


# PEDIDOS

def abrir_pedido(cliente_id, descricao_itens, peso_bolo, taxa_entrega, valor_total):
    conexao, cursor = conectar_banco()
    sql = '''
    insert into pedidos (cliente_id, descricao_itens, peso_bolo, taxa_entrega, valor_total, etapa)
    values (?, ?, ?, ?, ?, 'Recebido')
    '''
    cursor.execute(sql, (cliente_id, descricao_itens, peso_bolo, taxa_entrega, valor_total))
    conexao.commit()


def listar_pedidos_por_etapa(etapa):
    conexao, cursor = conectar_banco()
    sql = '''
    select pedidos.id, clientes.nome, clientes.endereco, pedidos.descricao_itens,
           pedidos.peso_bolo, pedidos.valor_total, motoboys.nome, motoboys.placa, pedidos.motoboy_id
    from pedidos
    join clientes on pedidos.cliente_id = clientes.id
    left join motoboys on pedidos.motoboy_id = motoboys.id
    where pedidos.etapa = ?
    '''
    cursor.execute(sql, (etapa,))
    resultados = cursor.fetchall()
    return resultados


def listar_todos_pedidos():
    conexao, cursor = conectar_banco()
    sql = '''
    select pedidos.id, pedidos.data_pedido, clientes.nome, clientes.endereco,
           pedidos.descricao_itens, motoboys.nome, pedidos.valor_total, pedidos.etapa
    from pedidos
    join clientes on pedidos.cliente_id = clientes.id
    left join motoboys on pedidos.motoboy_id = motoboys.id
    order by pedidos.id desc
    '''
    cursor.execute(sql)
    resultados = cursor.fetchall()
    return resultados


def preparar_pedido(id_pedido):
    conexao, cursor = conectar_banco()
    sql = '''
    update pedidos set etapa = 'Na Confeitaria' where id = ?
    '''
    cursor.execute(sql, (id_pedido,))
    conexao.commit()


def cancelar_pedido(id_pedido):
    conexao, cursor = conectar_banco()
    sql = '''
    update pedidos set etapa = 'Cancelado' where id = ?
    '''
    cursor.execute(sql, (id_pedido,))
    conexao.commit()


def despachar_pedido(id_pedido, id_motoboy):
    conexao, cursor = conectar_banco()
    cursor.execute("update pedidos set etapa = 'Saiu para Entrega', motoboy_id = ? where id = ?", (id_motoboy, id_pedido))
    cursor.execute("update motoboys set status = 'Em Rota' where id = ?", (id_motoboy,))
    conexao.commit()


def finalizar_entrega(id_pedido, id_motoboy):
    conexao, cursor = conectar_banco()
    cursor.execute("update pedidos set etapa = 'Entregue' where id = ?", (id_pedido,))
    if id_motoboy:
        cursor.execute("update motoboys set status = 'Disponível' where id = ?", (id_motoboy,))
    conexao.commit()