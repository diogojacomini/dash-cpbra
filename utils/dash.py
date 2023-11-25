import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import io
import base64


def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def get_data():
    dados_teste = {
        'temporada': [2020, 2021, 2022],
        'rodada': [35, 40, 37],
    }

    # Criar DataFrame pandas com os dados de teste
    df_teste = pd.DataFrame(dados_teste)

    return {'df_check': df_teste}


def plot_temporadas(dataset, x, y, cutoff=None):
    # Criar figura e eixos
    fig, ax = plt.subplots(figsize=(10, 4))

    # Criar gráfico de barras
    ax.bar(dataset[x], dataset[y], color='skyblue', align='center')

    if cutoff:
        ax.axhline(y=38, color='gray', linestyle='--', label='Limite de 38 jogos')
        for i, valor in enumerate(dataset[y]):
            if (valor < 38) and (dataset[x].iloc[i] != datetime.now().year):
                ax.text(dataset[x].iloc[i], valor + 0.2, str(valor), ha='center', va='bottom')
                ax.axhline(y=valor, color='red', linestyle='-')
            if (dataset[x].iloc[i] == datetime.now().year):
                ax.text(dataset[x].iloc[i], valor + 0.2, str(valor), ha='center', va='bottom')

    ax.set_title(f'Range de {x.title()}')
    ax.set_xlabel(x.title())
    ax.set_ylabel(y.title())
    ax.set_xticks(dataset[x])
    plt.tight_layout()  # Garante que o layout seja ajustado adequadamente
    return fig
