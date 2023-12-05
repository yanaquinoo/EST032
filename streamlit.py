import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Função para gerar amostras da Distribuição Binomial
def generate_binomial_samples(n, m, p):
    return [np.random.binomial(n, p, n) for _ in range(m)]

# Função para gerar amostras da Distribuição Exponencial
def generate_exponential_samples(n, m, lambd):
    return [np.random.exponential(1/lambd, n) for _ in range(m)]

# Função para gerar amostras da Distribuição Uniforme
def generate_uniform_samples(n, m, a, b):
    return [np.random.uniform(a, b, n) for _ in range(m)]

# Função para gerar amostras da Distribuição de Poisson
def generate_poisson_samples(m, lam):
    return [np.random.poisson(lam, m) for _ in range(m)]

# Função para gerar amostras da Distribuição Geométrica
def generate_geometric_samples(m, p):
    return [np.random.geometric(p, m) for _ in range(m)]

# # Função para gerar amostras da Distribuição de Weibull
# def generate_weibull_samples(m, shape, scale):
#     return [np.random.weibull(shape, m) * scale for _ in range(m)]

# Função para calcular as médias amostrais
def calculate_sample_means(samples):
    return [np.mean(sample) for sample in samples]

# Função para plotar histogramas
def plot_histogram(samples, sample_means, distribution, params):
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Define cores diferentes para cada distribuição
    colors = {
    'Binomial': 'green',
    'Exponencial': 'blue',
    'Uniforme': 'red',
    'Poisson': 'purple',  # Adicione a cor para a distribuição 'Poisson' aqui
    'Geométrica': 'orange'  # Adicione a cor para a distribuição 'Geométrica' aqui
}
  
    # Histograma das amostras com cores personalizadas
    sns.histplot(np.hstack(samples), bins=30, kde=True, color=colors[distribution], ax=ax[0])
    ax[0].set_title(f'Histograma das Amostras ({distribution})')

    # Histograma das médias amostrais com cores personalizadas
    sns.histplot(sample_means, bins=30, kde=True, color=colors[distribution], ax=ax[1])
    mean, std_dev = np.mean(sample_means), np.std(sample_means)

    # Calculate the bin width
    count, bins, ignored = ax[1].hist(sample_means, 30, density=True,alpha = 0)
    bin_width = bins[1] - bins[0]

    # Scale the PDF to the histogram height
    scale_factor = len(sample_means) * bin_width
    xmin, xmax = ax[1].get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mean, std_dev) * scale_factor  # Scale the PDF by the number of samples and the bin width

    ax[1].plot(x, p, 'k', linewidth=2)
    title = "Histograma das Médias Amostrais e Distribuição Normal"
    ax[1].set_title(title)

    return fig
# Layout
st.sidebar.title('Parâmetros de Entrada')
distribution = st.sidebar.selectbox('Selecione a Distribuição', ['Binomial', 'Exponencial', 'Uniforme', 'Poisson (extra)', 'Geométrica (extra)'])

st.title('Simulação de Distribuição de Probabilidade')
st.write('Esta ferramenta simula diferentes distribuições de probabilidade. Escolha a distribuição e parâmetros e clique em "Gerar e Plotar".')
    
if distribution == 'Binomial':
    st.sidebar.write("#### Distribuição Binomial")
    p = st.sidebar.slider('Probabilidade de Sucesso (p)', 0.0, 1.0, 0.5)
    n = st.sidebar.number_input('Tamanho da Amostra (n)', min_value=1, value=100)
    m = st.sidebar.number_input('Número de Amostras (m)', min_value=1, value=200)

    if st.sidebar.button('Gerar e Plotar'):
        samples = generate_binomial_samples(n, m, p)
        sample_means = calculate_sample_means(samples)
        fig = plot_histogram(samples, sample_means, 'Binomial', {'p': p})
        st.pyplot(fig)

        st.subheader(f'Comentários da Simulação - Binomial com p = {p}:')
        st.write(f'Nos gráficos acima é possível perceber a distribuição binomial com probabilidade igual a {p}. A distribuição Binomial é usada para modelar o número de sucessos em um processo de Bernoulli. Abaixo nós comparamos três cenários diferentes comuns dessa distribuição:')
        st.write('Nesta simulação da Distribuição Binomial, três conjuntos de experimentos foram realizados, cada um com uma probabilidade de sucesso (p) diferente. Aqui estão os resultados:')
        st.write('1. **Probabilidade de Sucesso Baixa (p = 0.1):** Quando a probabilidade de sucesso é baixa, a distribuição é fortemente assimétrica e deslocada para a esquerda. Isso significa que a maioria das amostras terá valores baixos, o que é consistente com uma baixa probabilidade de sucesso.')
        st.write('2. **Probabilidade de Sucesso Moderada (p = 0.5):** Quando a probabilidade de sucesso é igual a 0.5, a distribuição Binomial é simétrica. As amostras tendem a se concentrar em torno do valor médio, que é a metade do tamanho da amostra (n/2). Isso é esperado, pois a probabilidade de sucesso e fracasso é igual.')
        st.write('3. **Probabilidade de Sucesso Alta (p = 0.9):** Com uma alta probabilidade de sucesso, a distribuição é novamente assimétrica, mas agora deslocada para a direita. A maioria das amostras terá valores altos, o que é consistente com uma alta probabilidade de sucesso.')

elif distribution == 'Exponencial':
    st.sidebar.write("#### Distribuição Exponencial")
    lambd = st.sidebar.slider('Taxa (λ)', 0.1, 10.0, 1.0)
    n = st.sidebar.number_input('Tamanho da Amostra (n)', min_value=1, value=100)
    m = st.sidebar.number_input('Número de Amostras (m)', min_value=1, value=500)

    if st.sidebar.button('Gerar e Plotar'):
        samples = generate_exponential_samples(n, m, lambd)
        sample_means = calculate_sample_means(samples)
        fig = plot_histogram(samples, sample_means, 'Exponencial', {'λ': lambd})
        st.pyplot(fig)

        st.subheader('Comentários da Simulação - Distribuição Exponencial:')
        st.write('Para a Distribuição Exponencial, escolhemos um parâmetro de taxa (λ) igual a {p}. Esta distribuição é usada para modelar o tempo entre eventos em um processo de Poisson. Aqui estão os resultados:')
        st.write('1. **Distribuição Exponencial:** A distribuição Exponencial é caracterizada por uma cauda longa, o que significa que é provável observar valores pequenos, mas valores grandes são raros. Os histogramas das amostras refletem essa característica, com uma concentração maior de valores pequenos e uma queda acentuada na cauda direita.')
    

elif distribution == 'Poisson (extra)':
    st.sidebar.write("#### Distribuição de Poisson")
    lam = st.sidebar.slider('Taxa (λ)', 0.1, 100.0, 10.0)
    m = st.sidebar.number_input('Número de Amostras (m)', min_value=1, value=500)

    if st.sidebar.button('Gerar e Plotar'):
        samples = generate_poisson_samples(m, lam)
        sample_means = calculate_sample_means(samples)
        fig = plot_histogram(samples, sample_means, 'Poisson', {'λ': lam})
        st.pyplot(fig)

        st.subheader('Comentários da Simulação - Distribuição de Poisson:')
        st.write('A Distribuição de Poisson é usada para modelar a contagem de eventos raros em um intervalo fixo. Aqui estão os resultados:')
        # Adicione informações específicas sobre a Distribuição de Poisson aqui.

elif distribution == 'Geométrica (extra)':
    st.sidebar.write("#### Distribuição Geométrica")
    p = st.sidebar.slider('Probabilidade de Sucesso (p)', 0.0, 1.0, 0.15)
    m = st.sidebar.number_input('Número de Amostras (m)', min_value=1, value=500)

    if st.sidebar.button('Gerar e Plotar'):
        samples = generate_geometric_samples(m, p)
        sample_means = calculate_sample_means(samples)
        fig = plot_histogram(samples, sample_means, 'Geométrica', {'p': p})
        st.pyplot(fig)

        st.subheader('Comentários da Simulação - Distribuição Geométrica:')
        st.write('A Distribuição Geométrica modela o número de tentativas independentes até o primeiro sucesso em um processo de Bernoulli. Aqui estão os resultados:')
        # Adicione informações específicas sobre a Distribuição Geométrica aqui.

else:
    st.sidebar.write("#### Distribuição Uniforme")
    a = st.sidebar.slider('Limite Inferior (a)', 0.0, 10.0, 0.0)
    b = st.sidebar.slider('Limite Superior (b)', 0.0, 10.0, 1.0)
    n = st.sidebar.number_input('Tamanho da Amostra (n)', min_value=1, value=100)
    m = st.sidebar.number_input('Número de Amostras (m)', min_value=1, value=500)

    if st.sidebar.button('Gerar e Plotar'):
        samples = generate_uniform_samples(n, m, a, b)
        sample_means = calculate_sample_means(samples)
        fig = plot_histogram(samples, sample_means, 'Uniforme', {'a': a, 'b': b})
        st.pyplot(fig)

        st.subheader('Comentários da Simulação - Distribuição Uniforme:')
        st.write('Na simulação da Distribuição Uniforme, escolhemos um intervalo de [a, b] entre 0 e 5. Esta distribuição é caracterizada por ter a mesma probabilidade de qualquer valor dentro do intervalo. Aqui estão os resultados:')
        st.write('1. **Distribuição Uniforme:** Como esperado, a distribuição Uniforme apresenta uma distribuição uniforme de valores dentro do intervalo especificado [a, b]. Não há viés em direção a nenhum valor específico, e a frequência de ocorrência de valores é constante em todo o intervalo.')
