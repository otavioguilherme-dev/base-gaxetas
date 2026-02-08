import os
import subprocess
import sys

# Força a instalação do openpyxl se ele não for encontrado
try:
    import openpyxl
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])

import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd

# Configuração da página para Mobile e Desktop
st.set_page_config(page_title="Catálogo de Borrachas", layout="centered")

# Estilização básica para o cabeçalho
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🗂️ Consulta de Estoque e Medidas")
st.write("Busque pelo modelo da geladeira para ver medidas e SKUs.")

# Função para carregar sua base de 1000 linhas
@st.cache_data
def carregar_dados():
    # Simulação da sua planilha com as colunas reais
    data = {
        'MARCA': ['BRASTEMP', 'CONSUL', 'ELECTROLUX', 'CONTINENTAL', 'BRASTEMP'],
        'MODELO': ['BRM44', 'CRM33', 'RE31', 'RCV45', 'BRM44B'],
        'PERFIL': ['ENCAIXE', 'ABA', 'PARAFUSADA', 'ENCAIXE', 'ENCAIXE'],
        'MEDIDA GELADEIRA': ['68x115', '58x105', '55x90', '60x110', '68x120'],
        'MEDIDA FREEZER': ['68x40', '58x35', 'N/A', '60x40', '68x45'],
        'SKU GELADEIRA': ['BOR-001', 'BOR-055', 'BOR-099', 'BOR-201', 'BOR-002'],
        'SKU FREEZER': ['BOR-001-F', 'BOR-055-F', 'N/A', 'BOR-201-F', 'BOR-002-F']
    }
    return pd.DataFrame(data)

df = pd.read_excel("dados.xlsx", engine="openpyxl")

# Campo de busca (O modelo é a chave principal)
busca = st.text_input("Digite o MODELO:", placeholder="Ex: BRM44").upper().strip()

if busca:
    # Filtra modelos que contenham o texto digitado
    resultado = df[df['MODELO'].str.contains(busca)]
    
    if not resultado.empty:
        for index, row in resultado.iterrows():
            with st.expander(f"📍 {row['MARCA']} - {row['MODELO']}", expanded=True):
                st.subheader(f"Perfil: {row['PERFIL']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### ❄️ Freezer")
                    st.metric("Medida", row['MEDIDA FREEZER'])
                    st.caption(f"SKU: {row['SKU FREEZER']}")
                
                with col2:
                    st.markdown("### 🧊 Geladeira")
                    st.metric("Medida", row['MEDIDA GELADEIRA'])
                    st.caption(f"SKU: {row['SKU GELADEIRA']}")
                
                # Botão para copiar informações (útil para enviar no WhatsApp)
                texto_venda = f"Modelo: {row['MODELO']}\nMarca: {row['MARCA']}\nBorracha: {row['PERFIL']}\n\nMedida Freezer: {row['MEDIDA FREEZER']}\nMedida Geladeira: {row['MEDIDA GELADEIRA']}"
                st.code(texto_venda, language="text")
                st.caption("Copiando o texto acima, você pode colar no WhatsApp do cliente.")
    else:
        st.error("Nenhum modelo encontrado. Verifique a digitação.")

else:
    st.info("Aguardando busca... Digite o modelo acima.")
    # Mostra uma prévia da tabela geral se não houver busca
    with st.expander("Ver lista completa (Top 10)"):
        st.table(df.head(10))
