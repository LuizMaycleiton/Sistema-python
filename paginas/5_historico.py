import streamlit as st
import database as db

st.title("👥 Clientes & Histórico")

aba_cli, aba_hist = st.tabs(["Cadastro de Clientes", "Histórico de Pedidos"])

with aba_cli:
    c_form, c_lista = st.columns([1, 1.5], gap="large")
    with c_form:
        st.subheader("📝 Novo Cliente")
        with st.form("form_cliente", clear_on_submit=True):
            nome = st.text_input("Nome Completo")
            tel = st.text_input("Telefone / WhatsApp", placeholder="(11) 99999-0000")
            end = st.text_input("Endereço Completo", placeholder="Rua, Número, Bairro")
            if st.form_submit_button("Salvar Cliente", type="primary", use_container_width=True):
                if nome.strip() and end.strip():
                    db.cadastrar_cliente(nome.strip(), tel.strip(), end.strip())
                    st.success("Cliente cadastrado!")
                    st.rerun()
                else:
                    st.error("Nome e endereço são obrigatórios.")

    with c_lista:
        st.subheader("📋 Clientes Cadastrados")
        # c[0]=id, c[1]=nome, c[2]=telefone, c[3]=endereco
        for c in db.listar_clientes():
            with st.container(border=True):
                st.markdown(f"**{c[1]}** — 📞 {c[2]}")
                st.caption(f"📍 {c[3]}")

with aba_hist:
    st.subheader("📜 Histórico de Entregas e Pedidos")
    f1, f2 = st.columns([2, 1])
    busca_nome = f1.text_input("🔍 Buscar por Cliente:", placeholder="Digite o nome...")
    filtro_status = f2.selectbox("Status:", ["Todos", "Entregue", "Cancelado", "Recebido", "Na Confeitaria", "Saiu para Entrega"])
    
    pedidos = db.listar_todos_pedidos()
    # p[0]=id, p[1]=data, p[2]=cliente, p[3]=endereco, p[4]=itens, p[5]=motoboy, p[6]=total, p[7]=etapa
    for p in pedidos:
        if busca_nome and busca_nome.lower() not in p[2].lower():
            continue
        if filtro_status != "Todos" and p[7] != filtro_status:
            continue
            
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([2, 2.5, 1.2, 1.2])
            c1.markdown(f"**Pedido #{p[0]}** — {p[1][:16]}\n\n👤 {p[2]}")
            c2.write(f"🎂 {p[4]}\n\n📍 {p[3]}")
            c3.markdown(f"**R$ {p[6]:.2f}**\n\n🛵 {p[5] or '-'}")
            
            if p[7] == "Entregue":
                c4.success("Entregue")
            elif p[7] == "Cancelado":
                c4.error("Cancelado")
            else:
                c4.info(p[7])