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

# CONEXÃO COM A IA
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Usando o nome de modelo mais compatível para evitar o erro 'NotFound'
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro de Configuração: {e}")
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
            response = model.generate_content(f"Como estrategista logístico, analise: {relato}")
            st.info(response.text)
        else:
            st.warning("Por favor, descreva os custos antes de analisar.")

elif opcao == "Copiloto IA":
    st.title("🤖 Chat Estratégico")
    pergunta = st.chat_input("Pergunte algo sobre a estratégia da sua frota...")
    if pergunta:
        st.write(f"**Pergunta:** {pergunta}")
        try:
            response = model.generate_content(pergunta)
            st.write(f"**IA:** {response.text}")
        except Exception as e:
            st.error(f"A IA encontrou um problema ao responder: {e}")
