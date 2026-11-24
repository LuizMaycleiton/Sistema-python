import streamlit as st
import database as db

st.title("📊 Painel de Pedidos (Operação)")

recebidos = db.listar_pedidos_por_etapa("Recebido")
confeitaria = db.listar_pedidos_por_etapa("Na Confeitaria")
em_rota = db.listar_pedidos_por_etapa("Saiu para Entrega")
entregues = db.listar_pedidos_por_etapa("Entregue")

m1, m2, m3, m4 = st.columns(4)
m1.metric("📥 Recebidos", len(recebidos))
m2.metric("👩‍🍳 Na Confeitaria", len(confeitaria))
m3.metric("🛵 Saiu para Entrega", len(em_rota))
m4.metric("✅ Entregues (Total)", len(entregues))

st.divider()
col1, col2, col3 = st.columns(3, gap="medium")

# Índices de listar_pedidos_por_etapa:
# [0]=id, [1]=cliente_nome, [2]=endereco, [3]=descricao, [4]=peso, [5]=total, [6]=moto_nome, [7]=moto_placa, [8]=moto_id

with col1:
    st.subheader("📥 Recebidos")
    for p in recebidos:
        with st.container(border=True):
            st.markdown(f"**Pedido #{p[0]} — {p[1]}**")
            st.write(p[3])
            st.markdown(f"**Total: R$ {p[5]:.2f}**")
            b1, b2 = st.columns(2)
            if b1.button("➡️ Preparar", key=f"prep_{p[0]}", type="primary", use_container_width=True):
                db.preparar_pedido(p[0])
                st.rerun()
            if b2.button("❌ Cancelar", key=f"canc_{p[0]}", use_container_width=True):
                db.cancelar_pedido(p[0])
                st.rerun()

with col2:
    st.subheader("👩‍🍳 Na Confeitaria")
    for p in confeitaria:
        with st.container(border=True):
            st.markdown(f"**Pedido #{p[0]} — {p[1]}**")
            st.write(p[3])
            if p[4] > 2.0:
                st.warning(f"⚠️ Bolo de {p[4]} kg! Exige Baú Plano Grande.")
            
            motoboys_livres = db.listar_motoboys_disponiveis(p[4])
            if motoboys_livres:
                # m[0]=id, m[1]=nome, m[4]=tipo_bau
                opcoes_moto = {f"{m[1]} ({m[4]})": m[0] for m in motoboys_livres}
                escolha = st.selectbox("Motoboy Disponível:", list(opcoes_moto.keys()), key=f"moto_{p[0]}")
                if st.button("🛵 Despachar Entrega", key=f"desp_{p[0]}", type="primary", use_container_width=True):
                    db.despachar_pedido(p[0], opcoes_moto[escolha])
                    st.rerun()
            else:
                st.error("Nenhum motoboy compatível disponível.")

with col3:
    st.subheader("🛵 Saiu para Entrega")
    for p in em_rota:
        with st.container(border=True):
            st.markdown(f"**Pedido #{p[0]} — {p[1]}**")
            st.write(f"📍 **Endereço:** {p[2]}")
            st.write(f"🛵 **Motoboy:** {p[6]} ({p[7]})")
            st.markdown(f"**Total: R$ {p[5]:.2f}**")
            if st.button("✅ Confirmar Entrega", key=f"ent_{p[0]}", type="primary", use_container_width=True):
                db.finalizar_entrega(p[0], p[8])
                st.rerun()