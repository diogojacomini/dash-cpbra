import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import io
import base64
from utils.connect_az import AzureStore

az = AzureStore()

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def get_data():
    datasets = {'df_check': az.read_lake('campeonato-brasileiro', 'analytics/tb_sys_validacao_rodada.csv'),
                'df_check2': az.read_lake('campeonato-brasileiro', 'analytics/tb_sys_validacao_time.csv'),
                'counts': az.read_lake('campeonato-brasileiro', 'analytics/tb_sys_counts.csv'),
                }

    return datasets


def plot_temporadas(dataset, x, y, cutoff=None):
    # Criar figura e eixos
    fig, ax = plt.subplots(figsize=(16, 4))

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

    #ax.set_title(f'Range de {x.title()}')
    ax.set_xlabel(x.title())
    ax.set_ylabel(y.title())
    ax.set_xticks(dataset[x])
    plt.tight_layout()  # Garante que o layout seja ajustado adequadamente
    return fig
