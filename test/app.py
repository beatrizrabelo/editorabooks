import dash
from dash import html, dcc, Input, Output, State, dash_table, callback_context
import pandas as pd
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Caminho do arquivo CSV
CSV_PATH = 'livros.csv'

# Verifica se o arquivo CSV já existe, caso contrário, cria um novo com as colunas padrão
if os.path.exists(CSV_PATH):
    try:
        df_livros = pd.read_csv(CSV_PATH)
        # Garante que todas as colunas esperadas existam
        colunas_necessarias = ['Título', 'Autor', 'Gênero', 'Ano', 'Avaliação', 'Opinião']
        for col in colunas_necessarias:
            if col not in df_livros.columns:
                df_livros[col] = ''
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo CSV: {e}")
        df_livros = pd.DataFrame(columns=['Título', 'Autor', 'Gênero', 'Ano', 'Avaliação', 'Opinião'])
else:
    df_livros = pd.DataFrame(columns=['Título', 'Autor', 'Gênero', 'Ano', 'Avaliação', 'Opinião'])

# Criação do app Dash
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
    ],
    suppress_callback_exceptions=True
)

app.title = "Biblioteca Pessoal"
server = app.server  # Expõe o servidor Flask para o Gunicorn

# Layout do app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Layout da página inicial
def get_home_layout():
    # Calcula estatísticas para exibir no dashboard
    comentados = len(df_livros[df_livros['Opinião'].notna() & (df_livros['Opinião'] != '')])
    avaliacoes = df_livros['Avaliação'].apply(lambda x: int(x) if pd.notna(x) and x != '' and str(x).isdigit() else None)
    media_avaliacoes = avaliacoes.dropna().mean() if not avaliacoes.dropna().empty else 0
    
    # Contagem de gêneros para mostrar a distribuição
    generos = df_livros['Gênero'].value_counts().to_dict()
    
    return html.Div([
        html.Div([
            # Cabeçalho principal
            html.Div([
                html.H1("📚 Minha Biblioteca Pessoal", className="display-4 mb-4 text-center text-primary"),
                html.P("Gerencie sua coleção de livros, adicione avaliações e comentários", 
                       className="lead text-center mb-5")
            ]),
            
            # Dashboard com estatísticas
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(len(df_livros), className="display-4 text-primary"),
                            html.P("Livros Total", className="lead")
                        ], className="text-center p-3")
                    ], className="col-md-4 mb-4"),
                    
                    html.Div([
                        html.Div([
                            html.H3(f"{comentados}", className="display-4 text-success"),
                            html.P("Livros Comentados", className="lead")
                        ], className="text-center p-3")
                    ], className="col-md-4 mb-4"),
                    
                    html.Div([
                        html.Div([
                            html.H3(f"{media_avaliacoes:.1f} ⭐", className="display-4 text-warning"),
                            html.P("Avaliação Média", className="lead")
                        ], className="text-center p-3")
                    ], className="col-md-4 mb-4")
                ], className="row mb-4")
            ], className="p-4 bg-light rounded shadow-sm mb-5"),

            # Formulário para adicionar livros com design aprimorado
            html.Div([
                html.H3([html.I(className="fas fa-plus-circle me-2"), "Adicionar Novo Livro"], 
                         className="mb-4 text-center text-primary"),
                
                html.Div([
                    html.Div([
                        html.Label("Título", className="form-label fw-bold"),
                        dcc.Input(id='input-titulo', type='text', placeholder='Ex: Dom Casmurro', 
                                 className='form-control mb-3')
                    ], className="col-md-6"),
                    
                    html.Div([
                        html.Label("Autor", className="form-label fw-bold"),
                        dcc.Input(id='input-autor', type='text', placeholder='Ex: Machado de Assis', 
                                 className='form-control mb-3')
                    ], className="col-md-6"),
                    
                    html.Div([
                        html.Label("Gênero", className="form-label fw-bold"),
                        dcc.Input(id='input-genero', type='text', placeholder='Ex: Romance', 
                                 className='form-control mb-3')
                    ], className="col-md-6"),
                    
                    html.Div([
                        html.Label("Ano", className="form-label fw-bold"),
                        dcc.Input(id='input-ano', type='number', placeholder='Ex: 1899', 
                                 className='form-control mb-3', min=0, max=2100)
                    ], className="col-md-6"),
                ], className="row"),

                # Botão para adicionar livro
                html.Button([html.I(className="fas fa-plus me-2"), "Adicionar Livro"], 
                             id='botao-adicionar', 
                             className='btn btn-primary btn-lg mb-3 w-100'),
                             
                html.Div(id='validation-message', 
                         className='alert alert-danger d-none', 
                         children='Por favor, preencha todos os campos obrigatórios.')
            ], className="col-md-10 offset-md-1 p-4 border rounded bg-white shadow-sm mb-5"),

            # Tabela para exibir livros cadastrados
            html.Div([
                html.H3([html.I(className="fas fa-book me-2"), "Minha Coleção de Livros"], 
                         className="mb-4 text-primary"),
                html.Div([
                    html.Strong("Dica: "), 
                    "Clique em 'Ver detalhes' para avaliar um livro ou adicionar uma opinião."
                ], className="alert alert-info mb-3"),
                
                html.Div(id='total-livros', className="badge bg-primary fs-6 mb-3"),
                
                dash_table.DataTable(
                    id='tabela-livros',
                    columns=[
                        {'name': 'Título', 'id': 'Título'},
                        {'name': 'Autor', 'id': 'Autor'},
                        {'name': 'Gênero', 'id': 'Gênero'},
                        {'name': 'Ano', 'id': 'Ano'},
                        {'name': 'Avaliação', 'id': 'Avaliação Exibida', 'presentation': 'markdown'},
                        {'name': 'Status', 'id': 'Status', 'presentation': 'markdown'},
                        {'name': 'Ações', 'id': 'Ações', 'presentation': 'markdown'}
                    ],
                    data=[{
                        'Título': livro['Título'],
                        'Autor': livro['Autor'],
                        'Gênero': livro['Gênero'],
                        'Ano': livro['Ano'],
                        'Avaliação Exibida': '⭐' * int(livro['Avaliação']) if pd.notna(livro['Avaliação']) and livro['Avaliação'] != '' and str(livro['Avaliação']).isdigit() else '',
                        'Status': '✅ Comentado' if pd.notna(livro['Opinião']) and livro['Opinião'] != '' else '❌ Sem comentário',
                        'Ações': '[Ver detalhes](#)'
                    } for _, livro in df_livros.iterrows()],
                    style_cell={'textAlign': 'left', 'padding': '10px'},
                    style_header={
                        'backgroundColor': '#007bff', 
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'left'
                    },
                    style_table={'overflowX': 'auto'},
                    markdown_options={'html': True},
                    css=[{'selector': '.dash-cell div.dash-cell-value', 'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                    page_size=10
                )
            ], className="col-md-10 offset-md-1")
        ], className="container mt-4")
    ])

# Layout de detalhes do livro
def criar_layout_detalhes_livro(indice_livro):
    if indice_livro is None or int(indice_livro) >= len(df_livros):
        return html.Div([
            html.H3("Livro não encontrado", className="text-center mt-5"),
            html.Div([
                html.A("Voltar para a lista de livros", href="/", className="btn btn-primary")
            ], className="text-center mt-3")
        ], className="container")
    
    livro = df_livros.iloc[int(indice_livro)]
    
    # Calcula quantos livros têm comentários
    comentados = len(df_livros[df_livros['Opinião'].notna() & (df_livros['Opinião'] != '')])
    
    # Calcula a média de avaliações
    avaliacoes = df_livros['Avaliação'].apply(lambda x: int(x) if pd.notna(x) and x != '' and str(x).isdigit() else None)
    media_avaliacoes = avaliacoes.dropna().mean() if not avaliacoes.dropna().empty else 0
    
    # Formata a avaliação com estrelas
    avaliacao_estrelas = '⭐' * int(livro['Avaliação']) if pd.notna(livro['Avaliação']) and livro['Avaliação'] != '' and str(livro['Avaliação']).isdigit() else ''
    
    return html.Div([
        html.Div([
            # Botão de voltar
            html.Div([
                html.A([html.I(className="fas fa-arrow-left me-2"), "Voltar"], 
                       href="/", className="btn btn-outline-secondary mb-4")
            ]),
            
            # Detalhes do livro com design melhorado
            html.Div([
                html.Div([
                    html.H2(f"{livro['Título']}", className="mb-3 text-primary"),
                    html.Div([
                        html.Span(avaliacao_estrelas, className="fs-4 me-2"),
                        html.Span(f"({livro['Avaliação']})" if pd.notna(livro['Avaliação']) and livro['Avaliação'] != '' else "(Não avaliado)", className="text-muted")
                    ], className="mb-3"),
                    
                    # Informações do livro em um card
                    html.Div([
                        html.Div([
                            html.P([html.Strong("Autor: "), html.Span(livro['Autor'])], className="mb-2"),
                            html.P([html.Strong("Gênero: "), html.Span(livro['Gênero'])], className="mb-2"),
                            html.P([html.Strong("Ano: "), html.Span(livro['Ano'])], className="mb-2"),
                            
                            # Adiciona uma linha divisória
                            html.Hr(className="my-3"),
                            
                            # Estatísticas da biblioteca
                            html.P([html.Strong("Estatísticas da biblioteca:")], className="mb-2"),
                            html.P([html.I(className="fas fa-book me-2"), f"Total de livros: {len(df_livros)}"], className="mb-1 ms-3"),
                            html.P([html.I(className="fas fa-comment me-2"), f"Livros comentados: {comentados}"], className="mb-1 ms-3"),
                            html.P([html.I(className="fas fa-star me-2"), f"Média de avaliações: {media_avaliacoes:.1f}"], className="mb-1 ms-3")
                        ], className="card-body")
                    ], className="card mb-4 border-primary"),
                    
                    # Seção de opinião com destaque
                    html.Div([
                        html.H4([html.I(className="fas fa-quote-left me-2"), "Opinião sobre o livro:"], className="mb-3 text-primary"),
                        html.Div([
                            html.P(livro['Opinião'] if pd.notna(livro['Opinião']) and livro['Opinião'] != '' else 'Nenhuma opinião registrada.', 
                                  className="fst-italic" if pd.notna(livro['Opinião']) and livro['Opinião'] != '' else "text-muted")
                        ], className="p-3 bg-light rounded")
                    ], className="mb-4"),
                    
                    # Formulário para atualizar avaliação com design melhorado
                    html.Div([
                        html.H4([html.I(className="fas fa-edit me-2"), "Atualizar Avaliação e Opinião"], className="mb-3 text-primary"),
                        html.Div([
                            html.Label("Sua avaliação (1-5)", className="form-label fw-bold"),
                            dcc.Slider(
                                id='input-avaliacao',
                                min=1,
                                max=5,
                                step=1,
                                value=int(livro['Avaliação']) if pd.notna(livro['Avaliação']) and livro['Avaliação'] != '' and str(livro['Avaliação']).isdigit() else 3,
                                marks={i: f"{i} {'⭐' * i}" for i in range(1, 6)},
                                className="mb-4"
                            )
                        ]),
                        html.Div([
                            html.Label("Sua opinião sobre o livro", className="form-label fw-bold"),
                            dcc.Textarea(
                                id='input-opiniao',
                                value=livro['Opinião'] if pd.notna(livro['Opinião']) else '',
                                className="form-control mb-3",
                                placeholder="Compartilhe suas impressões sobre este livro...",
                                style={"height": "150px"}
                            )
                        ]),
                        html.Button([html.I(className="fas fa-save me-2"), "Salvar Alterações"], 
                                     id="botao-salvar", 
                                     className="btn btn-success w-100"),
                        html.Div(id="update-message", className="mt-3")
                    ], className="p-4 border rounded bg-light shadow-sm")
                ], className="col-12")
            ], className="p-4 bg-white rounded shadow")
        ], className="col-md-10 offset-md-1 mt-4 mb-5"),
        
        # Armazena o índice do livro atual
        dcc.Store(id='current-book-index', data=indice_livro)
    ], className="container")

# Callback para roteamento de páginas
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def exibir_pagina(pathname):
    if pathname == '/':
        return get_home_layout()
    
    # Verifica se o caminho é uma visualização de detalhes do livro
    if pathname.startswith('/livro/'):
        indice_livro = pathname.split('/')[-1]
        try:
            return criar_layout_detalhes_livro(int(indice_livro))
        except Exception as e:
            logger.error(f"Erro ao acessar detalhes do livro: {e}")
            return criar_layout_detalhes_livro(None)
            
    # Padrão - retorna à página inicial
    return get_home_layout()

# Callback para adicionar livro ao CSV e atualizar a tabela
@app.callback(
    [Output('tabela-livros', 'data'),
     Output('input-titulo', 'value'),
     Output('input-autor', 'value'),
     Output('input-genero', 'value'),
     Output('input-ano', 'value'),
     Output('validation-message', 'className')],
    Input('botao-adicionar', 'n_clicks'),
    [State('input-titulo', 'value'),
     State('input-autor', 'value'),
     State('input-genero', 'value'),
     State('input-ano', 'value'),
     State('tabela-livros', 'data')],
    prevent_initial_call=True
)
def adicionar_livro(n_clicks, titulo, autor, genero, ano, current_data):
    global df_livros
    
    # Verifica se os campos estão preenchidos
    if not titulo or not autor or not genero or not ano:
        # Prepare table data in the correct format
        table_data = [{
            'Título': livro['Título'],
            'Autor': livro['Autor'],
            'Gênero': livro['Gênero'],
            'Ano': livro['Ano'],
            'Avaliação Exibida': '⭐' * int(livro['Avaliação']) if pd.notna(livro['Avaliação']) and livro['Avaliação'] != '' and str(livro['Avaliação']).isdigit() else '',
            'Status': '✅ Comentado' if pd.notna(livro['Opinião']) and livro['Opinião'] != '' else '❌ Sem comentário',
            'Ações': '[Ver detalhes](#)'
        } for _, livro in df_livros.iterrows()]
        
        return (
            table_data,  # Retorna a tabela sem mudanças
            titulo, autor, genero, ano,
            'alert alert-danger'  # Mostra mensagem de validação
        )

    # Cria um novo livro e adiciona ao dataframe
    novo_livro = pd.DataFrame([{
        'Título': titulo,
        'Autor': autor,
        'Gênero': genero,
        'Ano': int(ano),
        'Avaliação': '',
        'Opinião': ''
    }])

    # Adiciona o novo livro ao dataframe
    df_livros = pd.concat([df_livros, novo_livro], ignore_index=True)
    
    # Salva o dataframe atualizado no CSV
    df_livros.to_csv(CSV_PATH, index=False)
    
    logger.debug(f"Livro adicionado: {titulo} por {autor}")

    # Prepare table data in the correct format
    table_data = [{
        'Título': livro['Título'],
        'Autor': livro['Autor'],
        'Gênero': livro['Gênero'],
        'Ano': livro['Ano'],
        'Avaliação Exibida': '⭐' * int(livro['Avaliação']) if pd.notna(livro['Avaliação']) and livro['Avaliação'] != '' and str(livro['Avaliação']).isdigit() else '',
        'Status': '✅ Comentado' if pd.notna(livro['Opinião']) and livro['Opinião'] != '' else '❌ Sem comentário',
        'Ações': '[Ver detalhes](#)'
    } for _, livro in df_livros.iterrows()]
    
    # Retorna os dados atualizados para o frontend
    return (
        table_data,
        '',  # Limpa o campo de título
        '',  # Limpa o campo de autor
        '',  # Limpa o campo de gênero
        '',  # Limpa o campo de ano
        'alert alert-danger d-none'  # Esconde a mensagem de validação
    )

# Callback para tratar cliques nas linhas da tabela
@app.callback(
    Output('url', 'pathname'),
    Input('tabela-livros', 'active_cell'),
    State('tabela-livros', 'data'),
    prevent_initial_call=True
)
def tratar_clique_tabela(active_cell, data):
    if active_cell:
        linha = active_cell['row']
        coluna = active_cell['column_id']
        
        # Só navega se a coluna "Ações" foi clicada
        if coluna == 'Ações':
            return f"/livro/{linha}"
    
    # Padrão: permanece na mesma página
    return dash.no_update

# Callback para atualizar avaliação e opinião do livro
@app.callback(
    [Output('update-message', 'children'),
     Output('update-message', 'className')],
    Input('botao-salvar', 'n_clicks'),
    [State('current-book-index', 'data'),
     State('input-avaliacao', 'value'),
     State('input-opiniao', 'value')],
    prevent_initial_call=True
)
def atualizar_avaliacao_livro(n_clicks, indice_livro, avaliacao, opiniao):
    global df_livros
    
    try:
        indice_livro = int(indice_livro)
        
        # Atualiza a avaliação e opinião do livro
        df_livros.at[indice_livro, 'Avaliação'] = avaliacao
        df_livros.at[indice_livro, 'Opinião'] = opiniao
        
        # Salva o dataframe atualizado no CSV
        df_livros.to_csv(CSV_PATH, index=False)
        
        logger.debug(f"Livro no índice {indice_livro} atualizado com avaliação {avaliacao}")
        
        # Retorna mensagem de sucesso
        return "Avaliação e opinião atualizadas com sucesso!", "alert alert-success"
    except Exception as e:
        logger.error(f"Erro ao atualizar livro: {e}")
        return f"Erro ao atualizar: {str(e)}", "alert alert-danger"

# Inicializa o contador de livros
@app.callback(
    Output('total-livros', 'children'),
    Input('tabela-livros', 'data')
)
def atualizar_contador_total(data):
    return f"Total: {len(data)} livros"

# Executar o servidor
if __name__ == '__main__':
    app.run(debug=True)