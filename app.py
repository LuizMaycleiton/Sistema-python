import os
import streamlit as st
import database as db

st.set_page_config(page_title="Atelier do Bolo", page_icon="🍰", layout="wide")

# Abre a conexão e garante as tabelas no modelo conectar_banco()
db.conectar_banco()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pg_painel = st.Page(os.path.join(BASE_DIR, "paginas", "1_painel.py"), title="Painel de Pedidos (Operação)", icon="📊", default=True)
pg_pedido = st.Page(os.path.join(BASE_DIR, "paginas", "2_novo_pedido.py"), title="Novo Pedido", icon="➕")
pg_catalogo = st.Page(os.path.join(BASE_DIR, "paginas", "3_catalogo.py"), title="Catálogo e Personalização", icon="🎂")
pg_motoboys = st.Page(os.path.join(BASE_DIR, "paginas", "4_motoboys.py"), title="Gestão de Motoboys", icon="🛵")
pg_historico = st.Page(os.path.join(BASE_DIR, "paginas", "5_historico.py"), title="Clientes & Histórico", icon="👥")

nav = st.navigation({
    "🍰 Atelier do Bolo": [pg_painel, pg_pedido, pg_catalogo, pg_motoboys, pg_historico]
})

st.sidebar.caption("Sistema de Gestão de Delivery")
nav.run()