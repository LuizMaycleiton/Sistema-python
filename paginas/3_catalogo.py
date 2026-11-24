import streamlit as st
import database as db

st.title("🎂 Catálogo e Personalização")

aba_produtos, aba_personalizacao = st.tabs([
    "Produtos Prontos & Bebidas", 
    "Massas, Recheios e Preço/kg"
])

with aba_produtos:
    col_form, col_lista = st.columns([1, 1.5], gap="large")

    with col_form:
        st.subheader("📝 Cadastrar Produto")
        with st.form("form_produto", clear_on_submit=True):
            nome = st.text_input("Nome do Produto", placeholder="Ex: Bolo Médio de Cenoura")
            categoria = st.selectbox("Categoria", ["Bolo Pequeno", "Bolo Médio", "Fatia", "Bebida"])
            preco = st.number_input("Preço Unitário (R$)", min_value=1.0, value=45.0, step=1.0)
            
            if st.form_submit_button("Salvar Produto", type="primary", use_container_width=True):
                if nome.strip():
                    db.cadastrar_produto(nome.strip(), categoria, preco)
                    st.success(f"'{nome}' cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("Informe o nome do produto.")

    with col_lista:
        st.subheader("📦 Produtos Cadastrados")
        produtos = db.listar_produtos()
        # p[0]=id, p[1]=nome, p[2]=categoria, p[3]=preco
        for p in produtos:
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1.2, 0.8])
                c1.markdown(f"**{p[1]}** — _{p[2]}_")
                c2.write(f"**R$ {p[3]:.2f}**")
                if c3.button("🗑️", key=f"del_prod_{p[0]}"):
                    db.excluir_produto(p[0])
                    st.rerun()

with aba_personalizacao:
    col_esq, col_dir = st.columns([1, 1.5], gap="large")

    with col_esq:
        st.subheader("📝 Nova Massa ou Recheio")
        with st.form("form_opcao", clear_on_submit=True):
            tipo = st.selectbox("Tipo de Cadastro", ["Massa", "Recheio"])
            nome_opcao = st.text_input("Nome da Opção", placeholder="Ex: Red Velvet / Leite Ninho")
            
            if st.form_submit_button("Salvar Opção", type="primary", use_container_width=True):
                if nome_opcao.strip():
                    db.cadastrar_opcao_bolo(tipo, nome_opcao.strip())
                    st.success(f"{tipo} '{nome_opcao}' salva!")
                    st.rerun()
                else:
                    st.error("Digite o nome da opção.")

        st.divider()
        st.subheader("💰 Preço Base por Quilo")
        preco_atual = db.obter_preco_kg()
        novo_preco_kg = st.number_input("Valor do kg (R$)", min_value=10.0, value=float(preco_atual), step=5.0)
        if st.button("Atualizar Preço por kg", use_container_width=True):
            db.atualizar_preco_kg(novo_preco_kg)
            st.success(f"Preço por kg atualizado para R$ {novo_preco_kg:.2f}!")
            st.rerun()

    with col_dir:
        st.subheader("🍰 Massas e Recheios Cadastrados")
        opcoes = db.listar_opcoes_bolo()
        # op[0]=id, op[1]=tipo, op[2]=nome
        for op in opcoes:
            with st.container(border=True):
                c1, c2, c3 = st.columns([1.2, 3, 0.8])
                c1.markdown(f"**{op[1]}**")
                c2.write(op[2])
                if c3.button("🗑️", key=f"del_op_{op[0]}"):
                    db.excluir_opcao_bolo(op[0])
                    st.rerun()