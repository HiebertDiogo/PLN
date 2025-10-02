# !pip install streamlit-folium
import os
import re
import json
import streamlit as st
import streamlit.components.v1 as components

def sanitize_filename(name):
    """
    Limpa o nome da residência para uso como nome de arquivo, removendo
    caracteres especiais e limitando o tamanho.
    """
    s = re.sub(r'[^\w\s-]', '', name).strip().lower()
    s = re.sub(r'[-\s]+', '_', s)
    return s[:60]


def salvar_mapa(mapa, nome_arquivo):
    pasta_saida = "resultados_mapas"
    os.makedirs(pasta_saida, exist_ok=True)
    caminho = os.path.join(pasta_saida, nome_arquivo)
    mapa.save(caminho)
    return caminho

# =======================================================================================

MAPS_DIR = "../mapas_individuais"

st.set_page_config(page_title="Imóvel e Vizinhança", layout="wide")
st.markdown("<h1 style='text-align: center;'>🏠 Analisador de Matrícula e Vizinhança</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 Envie o arquivo JSON do imóvel", type="json")

if uploaded_file:
    dados = json.load(uploaded_file)

    # Mostra resumo
    st.subheader("📑 Resumo do Imóvel")
    st.write(dados.get("resumo", "Nenhum resumo disponível."))

    # Procura o mapa salvo
    mapa_filename = f"mapa_{dados['matricula'].replace('.', '')}.html"
    mapa_path = os.path.join(MAPS_DIR, mapa_filename)

    st.subheader("🗺️ Mapa do Imóvel e Estabelecimentos Próximos")

    if os.path.exists(mapa_path):
        with open(mapa_path, "r", encoding="utf-8") as f:
            mapa_html = f.read()
        # Exibe centralizado
        col1, col2, col3 = st.columns([1,6,1])
        with col2:
            components.html(mapa_html, height=600, scrolling=False)
    else:
        st.warning(f"Mapa não encontrado para a matrícula {dados['matricula']} em {MAPS_DIR}.")
