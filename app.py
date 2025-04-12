import streamlit as st
import pandas as pd
from datetime import datetime
import os
if not os.path.exists('data'):
    os.makedirs('data')

DATA_PATH = 'data/analisePrevia.csv'

st.set_page_config(
    page_icon='📊', page_title='Análise Prévia', layout='centered')
st.title('Análise Prévia para a Publicação de Livros')

st.markdown('Preencha os dados abaixo para gerar a análise prévia.')

# Form's #

with st.form(key='analise_previa_form'):
    titulo = st.text_input('Título')
    autor = st.text_input('Autor')
    genero = st.selectbox('Gênero', ['Romance', 'Ficção Científica', 'Fantasia',
                                     'Terror', 'Fantasia', 'Aventura', 'Drama', 'Biografia', 'Auto-Ajuda', 'Outros'])

    publicoAlvo = st.selectbox(
        'Público Alvo', ['Infantil', 'Juvenil', 'Adulto'])
    paginasMedia = st.number_input(
        'Número de Páginas em Média', min_value=1, max_value=1000)
    valorMercado = st.number_input(
        'Valor Estimado do Mercado', min_value=0.0, format="%.2f")
    concorrentes = st.text_input('Concorrentes Relevantes (Autores/Editoras)')

    submit = st.form_submit_button('Salvar Análise')

    if submit:
        novaEntrada = {
            'Título': titulo,
            'Autor': autor,
            'Gênero': genero,
            'Público Alvo': publicoAlvo,
            'Número de Página em Média': paginasMedia,
            'Valor Estimado do Mercado': valorMercado,
            'Concorrentes Relevantes': concorrentes,
            'Data da Análise': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        try:
            df = pd.read_csv(DATA_PATH)
        except FileNotFoundError:
            df = pd.DataFrame()
        df = pd.contact([df, pd.dataFrame([novaEntrada])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        st.success('Análise salva com sucesso!')
