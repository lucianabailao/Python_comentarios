import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from textblob import TextBlob

# conexão banco
engine = create_engine("sqlite:///data/feedbacks.db")

st.title("Dashboard de Feedback de Clientes")

# carregar dados
df = pd.read_sql("SELECT * FROM feedbacks", engine)

st.write("### Dados atuais")
st.dataframe(df)

# gráfico
st.write("### Distribuição de Sentimentos")
sentimentos = df["sentimento"].value_counts()
st.bar_chart(sentimentos)

# -------------------------
# NOVO COMENTÁRIO
# -------------------------

st.write("## Adicionar novo comentário")

novo_comentario = st.text_area("Digite o feedback do cliente")

if st.button("Processar comentário com IA"):

    analise = TextBlob(novo_comentario)
    polaridade = analise.sentiment.polarity

    if polaridade > 0:
        sentimento = "Positivo"
        prioridade = "Baixa"
    elif polaridade < 0:
        sentimento = "Negativo"
        prioridade = "Alta"
    else:
        sentimento = "Neutro"
        prioridade = "Média"

    novo_df = pd.DataFrame([{
        "comentario": novo_comentario,
        "sentimento": sentimento,
        "prioridade": prioridade
    }])

    novo_df.to_sql("feedbacks", engine, if_exists="append", index=False)

    st.success("Comentário processado e salvo no banco!")

    st.rerun()
