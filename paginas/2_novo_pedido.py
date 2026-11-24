import streamlit as st
import database as db

st.title("➕ Novo Pedido")

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []
if "peso_total_pedido" not in st.session_state:
    st.session_state.peso_total_pedido = 0.0

col_cli, col_itens, col_resumo = st.columns([1, 1.3, 1.1], gap="medium")

with col_cli:
    with st.container(border=True):
        st.subheader("👤 Dados do Cliente")
        clientes = db.listar_clientes()
        # c[0]=id, c[1]=nome, c[2]=telefone, c[3]=endereco
        mapa_clientes = {f"{c[1]} - {c[2]}": c for c in clientes}
        sel_cliente = st.selectbox("Selecionar Cliente:", list(mapa_clientes.keys()))
        cliente_obj = mapa_clientes[sel_cliente]
        st.info(f"📍 **Endereço:** {cliente_obj[3]}")

with col_itens:
    with st.container(border=True):
        st.subheader("🎂 Adicionar Itens")
        aba_pers, aba_pronta = st.tabs(["Bolo Personalizado de Festa", "Pronta Entrega & Bebidas"])
        
        with aba_pers:
            # op[2]=nome
            massas = [m[2] for m in db.listar_opcoes_por_tipo("Massa")]
            recheios = [r[2] for r in db.listar_opcoes_por_tipo("Recheio")]
            preco_kg = db.obter_preco_kg()
            
            massa_sel = st.selectbox("Massa:", massas)
            recheio_sel = st.selectbox("Recheio:", recheios)
            peso = st.number_input("Peso (kg):", min_value=0.5, max_value=20.0, value=1.5, step=0.5)
            
            if peso > 2.0:
                st.warning("⚠️ ATENÇÃO: Bolo acima de 2,0 kg exige Baú Plano Grande.")
                
            obs_bolo = st.text_input("Observação / Plaquinha:", placeholder="Ex: Parabéns Sofia!")
            subtotal_bolo = peso * preco_kg
            st.caption(f"Valor calculado ({peso} kg x R$ {preco_kg:.2f}): **R$ {subtotal_bolo:.2f}**")
            
            if st.button("+ Adicionar Bolo Personalizado", type="primary", use_container_width=True):
                desc = f"Bolo Personalizado ({massa_sel}, {recheio_sel}, {peso} kg)"
                if obs_bolo:
                    desc += f" [Obs: {obs_bolo}]"
                st.session_state.carrinho.append({"desc": desc, "valor": subtotal_bolo, "peso": peso})
                st.session_state.peso_total_pedido = max(st.session_state.peso_total_pedido, peso)
                st.rerun()

        with aba_pronta:
            produtos = db.listar_produtos()
            # p[0]=id, p[1]=nome, p[2]=categoria, p[3]=preco
            mapa_prod = {f"{p[1]} - R$ {p[3]:.2f}": p for p in produtos}
            prod_sel = st.selectbox("Selecionar Produto / Bebida:", list(mapa_prod.keys()))
            qtd = st.number_input("Quantidade:", min_value=1, value=1, step=1)
            
            if st.button("+ Adicionar ao Pedido", type="primary", use_container_width=True):
                p_obj = mapa_prod[prod_sel]
                st.session_state.carrinho.append({
                    "desc": f"{qtd}x {p_obj[1]}",
                    "valor": p_obj[3] * qtd,
                    "peso": 0.0
                })
                st.rerun()

with col_resumo:
    with st.container(border=True):
        st.subheader("🧾 Resumo do Pedido")
        if not st.session_state.carrinho:
            st.caption("Nenhum item adicionado ainda.")
        else:
            soma_itens = 0.0
            for idx, item in enumerate(st.session_state.carrinho):
                c_txt, c_del = st.columns([4, 1])
                c_txt.write(f"• {item['desc']} — **R$ {item['valor']:.2f}**")
                if c_del.button("🗑️", key=f"rem_{idx}"):
                    st.session_state.carrinho.pop(idx)
                    st.session_state.peso_total_pedido = max([i["peso"] for i in st.session_state.carrinho], default=0.0)
                    st.rerun()
                soma_itens += item["valor"]
            
            st.divider()
            taxa = st.number_input("Taxa de Entrega (R$):", min_value=0.0, value=8.0, step=1.0)
            total_final = soma_itens + taxa
            st.markdown(f"### Total: R$ {total_final:.2f}")
            
            if st.button("💾 Finalizar e Enviar Pedido", type="primary", use_container_width=True):
                descricao_geral = " | ".join([i["desc"] for i in st.session_state.carrinho])
                db.abrir_pedido(
                    cliente_obj[0],
                    descricao_geral,
                    st.session_state.peso_total_pedido,
                    taxa,
                    total_final
                )
                st.session_state.carrinho = []
                st.session_state.peso_total_pedido = 0.0
                st.success("✅ Pedido enviado para o Painel de Operação!")
                st.rerun()