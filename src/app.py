from textblob import TextBlob
import pandas as pd
from sqlalchemy import create_engine

# Conectar ao banco SQLite
engine = create_engine("sqlite:///data/feedbacks.db")

# Lista de comentários simulando clientes
comentarios = [
    "Adorei o atendimento da empresa",
    "O produto chegou com defeito",
    "Entrega foi rápida",
    "Estou muito insatisfeito com o suporte",
    "O serviço é bom",
    "O atendimento foi horrível"
]

# palavras para reforçar classificação em português
palavras_negativas = [
    "horrível",
    "péssimo",
    "ruim",
    "insatisfeito",
    "problema",
    "defeito",
    "demora",
    "reclamação",
    "atraso"
]

palavras_positivas = [
    "ótimo",
    "excelente",
    "bom",
    "gostei",
    "adorei",
    "perfeito",
    "rápido"
]

dados = []

for comentario in comentarios:

    analise = TextBlob(comentario)
    polaridade = analise.sentiment.polarity

    texto = comentario.lower()

    # classificação com regras + IA
    if any(p in texto for p in palavras_negativas):
        sentimento = "Negativo"
        prioridade = "Alta"

    elif any(p in texto for p in palavras_positivas):
        sentimento = "Positivo"
        prioridade = "Baixa"

    else:
        if polaridade > 0:
            sentimento = "Positivo"
            prioridade = "Baixa"
        elif polaridade < 0:
            sentimento = "Negativo"
            prioridade = "Alta"
        else:
            sentimento = "Neutro"
            prioridade = "Média"

    dados.append({
        "comentario": comentario,
        "sentimento": sentimento,
        "prioridade": prioridade
    })

df = pd.DataFrame(dados)

# salvar no banco
df.to_sql("feedbacks", engine, if_exists="replace", index=False)

print("Dados salvos com sucesso no banco!")
