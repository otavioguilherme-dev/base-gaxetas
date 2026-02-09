import streamlit as st
import pandas as pd
from PIL import Image
import os

# CONFIGURAÇÃO DA PÁGINA (Título que aparece na aba do navegador)
st.set_page_config(
    page_title="Sistema de Consulta  de Modelos - OGNET BORRACHAS", 
    page_icon="❄️", 
    layout="wide"
)

# --- PERSONALIZAÇÃO DE CORES (Opcional) ---
# Você pode mudar o 'primaryColor' nas configurações do Streamlit Cloud,
# mas aqui vamos focar no visual da página.

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel("dados.xlsx", engine="openpyxl")
        df.columns = df.columns.str.strip().str.upper()
        df = df.astype(str).replace('nan', '') 
        for col in df.columns:
            df[col] = df[col].str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o Excel: {e}")
        return None

# --- CABEÇALHO PERSONALIZADO ---
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    # Verifica se o arquivo de logo existe no GitHub
    if os.path.exists("logo.png"):
        image = Image.open("logo.png")
        st.image(image, width=150)
    else:
        st.write("🚀") # Ícone padrão caso não ache a logo

with col_titulo:
    st.title("OGNET BORRACHAS")
    st.subheader("Catálogo Digital de Borrachas e Gaxetas")

st.markdown("---")


st.set_page_config(page_title="Catálogo Profissional de Borrachas", layout="wide")

# Estilo para melhorar a visualização no celular
st.markdown("""
    <style>
    .stDataFrame { border: 1px solid #e6e9ef; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel("dados.xlsx", engine="openpyxl")
        df.columns = df.columns.str.strip().str.upper()
        df = df.astype(str).replace('nan', '') 
        for col in df.columns:
            df[col] = df[col].str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o Excel: {e}")
        return None

df = carregar_dados()

if df is not None:
    # --- BARRA LATERAL (SIDEBAR) ---
    st.sidebar.header("Filtros de Marca")
    
    # Opção para selecionar a marca
    marcas_disponiveis = sorted(df['MARCA'].unique())
    marca_selecionada = st.sidebar.selectbox(
        "Selecione a Marca:",
        options=["TODAS"] + marcas_disponiveis
    )

    if st.sidebar.button("Limpar Filtros"):
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.info("Utilize a busca principal para pesquisar por MODELO ou MEDIDA simultaneamente.")

    # --- ÁREA PRINCIPAL ---
    st.title("🔍 Consulta de Borrachas")
    
    termo_busca = st.text_input(
        "Busca rápida (Modelo ou Medida):", 
        placeholder="Ex: BRM44 ou 68x115"
    ).upper().strip()

    # Aplicação dos Filtros
    df_filtrado = df.copy()

    # Filtro de Marca (se não for "TODAS")
    if marca_selecionada != "TODAS":
        df_filtrado = df_filtrado[df_filtrado['MARCA'] == marca_selecionada]

    # Filtro de Termo (Modelo ou Medida)
    if termo_busca:
        mask = (
            df_filtrado['MODELO'].str.contains(termo_busca, na=False) |
            df_filtrado['MEDIDA GELADEIRA'].str.contains(termo_busca, na=False) |
            df_filtrado['MEDIDA FREEZER'].str.contains(termo_busca, na=False)
        )
        df_filtrado = df_filtrado[mask]

    # Exibição dos Resultados
    if not df_filtrado.empty:
        st.success(f"Encontrado(s) {len(df_filtrado)} item(ns)")
        
        # Mostra a tabela com os resultados
        st.dataframe(
            df_filtrado, 
            use_container_width=True, 
            hide_index=True,
            column_order=("MARCA", "MODELO", "PERFIL", "MEDIDA GELADEIRA", "MEDIDA FREEZER", "SKU GELADEIRA", "SKU FREEZER")
        )
        
        # Se o filtro resultar em poucos itens, mostra os cards de detalhes
        if 0 < len(df_filtrado) <= 3:
            for _, row in df_filtrado.iterrows():
                with st.chat_message("assistant"):
                    st.write(f"**RESUMO PARA WHATSAPP - {row['MODELO']}**")
                    texto = (f"Marca: {row['MARCA']}\n"
                             f"Modelo: {row['MODELO']}\n"
                             f"Perfil: {row['PERFIL']}\n"
                             f"Medida Geladeira: {row['MEDIDA GELADEIRA']} (SKU: {row['SKU GELADEIRA']})\n"
                             f"Medida Freezer: {row['MEDIDA FREEZER']} (SKU: {row['SKU FREEZER']})")
                    st.code(texto, language="text")
    else:
        st.warning("Nenhum resultado encontrado para os filtros selecionados.")

else:
    st.error("Erro crítico: Verifique se o arquivo 'dados.xlsx' está no GitHub.")
