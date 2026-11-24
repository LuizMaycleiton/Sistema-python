import streamlit as st
import database as db

st.title("🛵 Gestão de Motoboys")

col_form, col_equipe = st.columns([1, 1.8], gap="large")

with col_form:
    st.subheader("📝 Cadastrar Motoboy")
    with st.form("form_motoboy", clear_on_submit=True):
        nome = st.text_input("Nome Completo")
        telefone = st.text_input("Telefone", placeholder="(11) 99999-9999")
        placa = st.text_input("Placa da Moto", placeholder="ABC-1234")
        tipo_bau = st.selectbox("Tipo de Baú", ["Baú Padrão", "Baú Plano Grande"])
        
        if st.form_submit_button("Salvar Motoboy", type="primary", use_container_width=True):
            if nome.strip() and placa.strip():
                db.cadastrar_motoboy(nome.strip(), telefone.strip(), placa.strip().upper(), tipo_bau)
                st.success(f"Motoboy {nome} cadastrado!")
                st.rerun()
            else:
                st.error("Nome e placa são obrigatórios.")

with col_equipe:
    st.subheader("👥 Equipe de Entregas")
    motoboys = db.listar_motoboys()
    # m[0]=id, m[1]=nome, m[2]=telefone, m[3]=placa, m[4]=tipo_bau, m[5]=status
    cols = st.columns(2)
    for idx, m in enumerate(motoboys):
        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"### {m[1]}")
                st.write(f"**Placa:** {m[3]} | **Tel:** {m[2]}")
                
                if m[4] == "Baú Plano Grande":
                    st.warning(f"📦 {m[4]}")
                else:
                    st.info(f"📦 {m[4]}")
                
                if m[5] == "Em Rota":
                    st.warning("🟡 Status: **Em Rota** (Entrega em andamento)")
                else:
                    opcoes_status = ["Disponível", "Indisponível"]
                    indice_atual = opcoes_status.index(m[5]) if m[5] in opcoes_status else 0
                    novo_status = st.selectbox(
                        "Alterar Status:",
                        opcoes_status,
                        index=indice_atual,
                        key=f"status_moto_{m[0]}"
                    )
                    if novo_status != m[5]:
                        db.alterar_status_motoboy(m[0], novo_status)
                        st.rerun()