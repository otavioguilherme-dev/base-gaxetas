import streamlit as st
import pandas as pd

st.set_page_config(page_title="Catálogo de Borrachas", layout="wide")

st.title("🗂️ Consulta de Estoque e Medidas")

@st.cache_data
def carregar_dados():
    try:
        # Carrega o arquivo Excel
        df = pd.read_excel("dados.xlsx", engine="openpyxl")
        
        # PADRONIZAÇÃO TOTAL:
        # 1. Limpa nomes de colunas (tira espaços e põe em maiúsculo)
        df.columns = df.columns.str.strip().str.upper()
        
        # 2. Converte toda a tabela para TEXTO e remove espaços em branco
        # Isso evita o erro de números ou células vazias
        df = df.astype(str).replace('nan', '') 
        for col in df.columns:
            df[col] = df[col].str.strip()
            
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o Excel: {e}")
        return None

df = carregar_dados()

if df is not None:
    # Interface de busca
    busca = st.text_input("Digite o MODELO para pesquisar:", placeholder="Ex: BRM44").upper().strip()

    if busca:
        # O segredo da correção está aqui: na_msg=False e garantir que a coluna existe
        if 'MODELO' in df.columns:
            # Filtra ignorando erros de valores nulos
            mask = df['MODELO'].str.contains(busca, case=False, na=False)
            resultado = df[mask]
            
            if not resultado.empty:
                st.success(f"Encontrado(s) {len(resultado)} item(ns):")
                
                # Exibe os resultados formatados
                for _, row in resultado.iterrows():
                    with st.expander(f"📍 {row['MARCA']} - {row['MODELO']}", expanded=True):
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.write(f"**Perfil:** {row['PERFIL']}")
                        with c2:
                            st.write(f"**Geladeira:** {row.get('MEDIDA GELADEIRA', 'N/A')}")
                            st.caption(f"SKU: {row.get('SKU GELADEIRA', '-')}")
                        with c3:
                            st.write(f"**Freezer:** {row.get('MEDIDA FREEZER', 'N/A')}")
                            st.caption(f"SKU: {row.get('SKU FREEZER', '-')}")
            else:
                st.warning("Nenhum modelo encontrado com esse nome.")
        else:
            st.error("Coluna 'MODELO' não encontrada. Verifique o cabeçalho do seu Excel.")
    else:
        st.info("💡 Dica: Digite parte do modelo para ver todos os resultados relacionados.")
