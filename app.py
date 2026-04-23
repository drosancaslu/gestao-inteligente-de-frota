import streamlit as st
import google.generativeai as genai

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Portal de Inteligência Logística", layout="wide")

# LOGIN SIMPLES
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("Acesso Restrito - Consultoria IA")
    senha = st.text_input("Introduza a Chave de Acesso:", type="password")
    if st.button("Entrar"):
        if senha == "freitas123":
            st.session_state["autenticado"] = True
            st.rerun()
    st.stop()

# CONEXÃO COM A IA (COM AUTODETECÇÃO)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Tenta o modelo Flash, se falhar, tenta o Pro
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Teste rápido para ver se o modelo existe
        model.prepare_content_request(contents="test")
    except:
        model = genai.GenerativeModel('gemini-pro')
        
except Exception as e:
    st.error(f"Erro de Conexão: {e}")
    st.stop()

# INTERFACE
st.sidebar.title("MENU LOGÍSTICO")
opcao = st.sidebar.radio("Ir para:", ["Análise de Custos", "Copiloto IA"])

if opcao == "Análise de Custos":
    st.title("📊 Análise Operacional")
    st.write("Diga à IA os gastos do mês para receber um diagnóstico.")
    relato = st.text_area("Descreva os custos ou problemas detectados:")
    if st.button("Analisar"):
        if relato:
            try:
                response = model.generate_content(f"Como estrategista logístico, analise: {relato}")
                st.info(response.text)
            except Exception as e:
                st.error(f"Erro na análise: {e}")
        else:
            st.warning("Por favor, preencha o relato.")

elif opcao == "Copiloto IA":
    st.title("🤖 Chat Estratégico")
    pergunta = st.chat_input("Pergunte algo...")
    if pergunta:
        st.write(f"**Sua Pergunta:** {pergunta}")
        try:
            response = model.generate_content(pergunta)
            st.write(f"**IA:** {response.text}")
        except Exception as e:
            st.error(f"O modelo encontrou um problema: {e}")
