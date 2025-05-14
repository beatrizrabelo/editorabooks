import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import random
import requests
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

# Configuração da página
st.set_page_config(
    page_title="BiblioTech - Sua Biblioteca Digital",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cores e tema
PRIMARY_COLOR = "#7c3aed"  # Roxo vibrante
SECONDARY_COLOR = "#5b21b6"  # Roxo mais escuro
ACCENT_COLOR = "#ec4899"  # Rosa
BG_COLOR = "#f8fafc"  # Cinza claro
CARD_BG_COLOR = "#ffffff"  # Branco
TEXT_COLOR = "#1e293b"  # Cinza escuro
SIDEBAR_COLOR = "#f1f5f9"  # Cinza muito claro

# Função para carregar animações Lottie
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Carregar animações
lottie_book = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_1a8dx7zj.json")
lottie_reading = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_qmfs6c3i.json")
lottie_library = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_ystsffqy.json")

# Aplicar CSS personalizado para melhorar a aparência
st.markdown(f"""
<style>
    /* Estilos gerais */
    .main {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Poppins', sans-serif;
    }}
    
    .stApp {{
        max-width: 1400px;
        margin: 0 auto;
    }}
    
    h1, h2, h3, h4, h5 {{
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: {PRIMARY_COLOR};
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {SIDEBAR_COLOR};
        border-right: 1px solid #e2e8f0;
    }}
    
    /* Cards de livros */
    .book-card {{
        background-color: {CARD_BG_COLOR};
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
        transition: all 0.4s ease;
        border: 1px solid #f1f5f9;
        display: flex;
        flex-direction: column;
        height: 100%;
        overflow: hidden;
        position: relative;
    }}
    
    .book-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 30px rgba(0,0,0,0.08);
        border-color: {PRIMARY_COLOR}40;
    }}
    
    .book-cover {{
        width: 100%;
        height: 240px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }}
    
    .book-card:hover .book-cover {{
        transform: scale(1.03);
    }}
    
    .book-title {{
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 8px;
        color: {PRIMARY_COLOR};
        line-height: 1.3;
    }}
    
    .book-author {{
        font-style: italic;
        color: #64748b;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }}
    
    .book-meta {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        color: #64748b;
        font-size: 0.9rem;
    }}
    
    .book-rating {{
        font-weight: bold;
        color: #f59e0b;
        font-size: 1.2rem;
        margin-top: 10px;
    }}
    
    .book-description {{
        color: #64748b;
        font-size: 0.95rem;
        margin-top: 10px;
        flex-grow: 1;
    }}
    
    .book-button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}, {SECONDARY_COLOR});
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 15px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        margin-top: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(124, 58, 237, 0.2);
    }}
    
    .book-button:hover {{
        box-shadow: 0 6px 12px rgba(124, 58, 237, 0.3);
        transform: translateY(-2px);
    }}
    
    /* Detalhes do livro */
    .book-detail-container {{
        background-color: {CARD_BG_COLOR};
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-top: 20px;
        border: 1px solid #f1f5f9;
    }}
    
    .book-detail-cover {{
        width: 100%;
        max-height: 450px;
        object-fit: cover;
        border-radius: 12px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }}
    
    .book-detail-title {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {PRIMARY_COLOR};
        margin-bottom: 10px;
        line-height: 1.2;
    }}
    
    .book-detail-author {{
        font-size: 1.5rem;
        font-style: italic;
        color: #64748b;
        margin-bottom: 20px;
    }}
    
    .book-detail-meta {{
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
        color: #64748b;
    }}
    
    .book-detail-rating {{
        font-size: 1.5rem;
        color: #f59e0b;
        margin-bottom: 20px;
    }}
    
    .book-detail-synopsis {{
        font-size: 1.1rem;
        line-height: 1.8;
        color: #334155;
        margin-bottom: 30px;
        background-color: #f8fafc;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid {PRIMARY_COLOR};
    }}
    
    /* Comentários */
    .comment-section {{
        margin-top: 40px;
    }}
    
    .comment-box {{
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 4px solid {ACCENT_COLOR};
        transition: transform 0.2s ease;
    }}
    
    .comment-box:hover {{
        transform: translateX(5px);
    }}
    
    .comment-author {{
        font-weight: bold;
        color: {PRIMARY_COLOR};
        font-size: 1.1rem;
    }}
    
    .comment-date {{
        font-size: 0.85rem;
        color: #94a3b8;
        margin-bottom: 10px;
    }}
    
    .comment-content {{
        font-size: 1rem;
        line-height: 1.6;
        color: #334155;
    }}
    
    /* Formulários */
    .form-container {{
        background-color: {CARD_BG_COLOR};
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.03);
        margin-bottom: 25px;
        border: 1px solid #f1f5f9;
    }}
    
    .form-title {{
        font-size: 1.5rem;
        color: {PRIMARY_COLOR};
        margin-bottom: 20px;
        border-bottom: 2px solid {PRIMARY_COLOR}40;
        padding-bottom: 10px;
    }}
    
    /* Botões */
    .stButton > button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}, {SECONDARY_COLOR});
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 4px 6px rgba(124, 58, 237, 0.2) !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(124, 58, 237, 0.3) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}
    
    /* Destaque para livros populares */
    .featured-section {{
        margin-bottom: 40px;
    }}
    
    .featured-title {{
        font-size: 1.8rem;
        color: {PRIMARY_COLOR};
        margin-bottom: 25px;
        border-bottom: 3px solid {PRIMARY_COLOR};
        padding-bottom: 10px;
        display: inline-block;
    }}
    
    /* Barra de navegação */
    .nav-container {{
        margin-bottom: 25px;
    }}
    
    /* Badges */
    .badge {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}, {ACCENT_COLOR});
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 5px;
        box-shadow: 0 2px 5px rgba(124, 58, 237, 0.2);
    }}
    
    /* Banner */
    .banner {{
        background: linear-gradient(135deg, {PRIMARY_COLOR}, {SECONDARY_COLOR});
        border-radius: 20px;
        padding: 40px;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .banner::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('https://www.transparenttextures.com/patterns/cubes.png');
        opacity: 0.1;
    }}
    
    .banner h1 {{
        color: white;
        font-size: 2.5rem;
        margin-bottom: 15px;
        font-weight: 700;
    }}
    
    .banner p {{
        font-size: 1.2rem;
        margin-bottom: 25px;
        opacity: 0.9;
    }}
    
    .banner-button {{
        background-color: white;
        color: {PRIMARY_COLOR};
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        display: inline-block;
        margin-right: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .banner-button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}
    
    .banner-button-outline {{
        background-color: transparent;
        color: white;
        border: 2px solid white;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        display: inline-block;
    }}
    
    .banner-button-outline:hover {{
        background-color: white;
        color: {PRIMARY_COLOR};
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}
    
    /* Stats cards */
    .stats-card {{
        background-color: white;
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        border: 1px solid #f1f5f9;
    }}
    
    .stats-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-color: {PRIMARY_COLOR}40;
    }}
    
    .stats-icon {{
        font-size: 2rem;
        color: {PRIMARY_COLOR};
        margin-bottom: 15px;
    }}
    
    .stats-number {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {PRIMARY_COLOR};
        margin-bottom: 5px;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, {ACCENT_COLOR});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    .stats-label {{
        color: #64748b;
        font-size: 1rem;
    }}
    
    /* Animações */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .animate-fade-in {{
        animation: fadeIn 0.5s ease-out forwards;
    }}
    
    /* Delay para animações em sequência */
    .delay-1 {{ animation-delay: 0.1s; }}
    .delay-2 {{ animation-delay: 0.2s; }}
    .delay-3 {{ animation-delay: 0.3s; }}
    .delay-4 {{ animation-delay: 0.4s; }}
    .delay-5 {{ animation-delay: 0.5s; }}
    
    /* Responsividade */
    @media (max-width: 768px) {{
        .book-card {{
            padding: 15px;
        }}
        
        .book-title {{
            font-size: 1.2rem;
        }}
        
        .book-cover {{
            height: 180px;
        }}
        
        .banner {{
            padding: 25px;
        }}
        
        .banner h1 {{
            font-size: 1.8rem;
        }}
    }}
    
    /* Estilização de inputs */
    .stTextInput > div > div > input {{
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 10px 15px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {PRIMARY_COLOR} !important;
        box-shadow: 0 0 0 2px {PRIMARY_COLOR}40 !important;
    }}
    
    .stTextArea > div > div > textarea {{
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 10px 15px !important;
    }}
    
    .stTextArea > div > div > textarea:focus {{
        border-color: {PRIMARY_COLOR} !important;
        box-shadow: 0 0 0 2px {PRIMARY_COLOR}40 !important;
    }}
    
    .stSelectbox > div > div > div {{
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
    }}
    
    .stSelectbox > div > div > div:focus {{
        border-color: {PRIMARY_COLOR} !important;
        box-shadow: 0 0 0 2px {PRIMARY_COLOR}40 !important;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 20px;
        color: #64748b;
        margin-top: 50px;
        border-top: 1px solid #e2e8f0;
    }}
    
    /* Glassmorphism effect */
    .glass-card {{
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
</style>

<!-- Importar fontes -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

# Inicialização do banco de dados
def init_db():
    """Inicializa o banco de dados SQLite com as tabelas necessárias."""
    conn = sqlite3.connect('biblioteca.db')
    c = conn.cursor()
    
    # Criar tabela de livros se não existir
    c.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER,
        genero TEXT,
        sinopse TEXT,
        nota REAL,
        data_adicao TEXT,
        capa_url TEXT
    )
    ''')
    
    # Criar tabela de comentários se não existir
    c.execute('''
    CREATE TABLE IF NOT EXISTS comentarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        livro_id INTEGER,
        nome_usuario TEXT,
        comentario TEXT,
        data_comentario TEXT,
        FOREIGN KEY (livro_id) REFERENCES livros (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Função para adicionar livros populares pré-definidos
def adicionar_livros_populares():
    """Adiciona alguns livros populares ao banco de dados se ainda não existirem."""
    conn = sqlite3.connect('biblioteca.db')
    c = conn.cursor()
    
    # Verificar se já existem livros no banco
    c.execute("SELECT COUNT(*) FROM livros")
    count = c.fetchone()[0]
    
    if count == 0:
        # Lista de livros populares para adicionar
        livros_populares = [
            {
                "titulo": "Cem Anos de Solidão",
                "autor": "Gabriel García Márquez",
                "ano_publicacao": 1967,
                "genero": "Realismo Mágico",
                "sinopse": "Uma das obras mais importantes da literatura mundial, conta a história da família Buendía ao longo de várias gerações na fictícia cidade de Macondo. A narrativa mistura realidade e fantasia, explorando temas como solidão, amor, guerra e o destino cíclico da humanidade.",
                "nota": 4.8,
                "capa_url": "https://m.media-amazon.com/images/I/81G+l+iMm+L._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "1984",
                "autor": "George Orwell",
                "ano_publicacao": 1949,
                "genero": "Ficção Distópica",
                "sinopse": "Ambientado em um futuro distópico onde o governo totalitário, liderado pelo enigmático Grande Irmão, controla todos os aspectos da vida dos cidadãos, incluindo seus pensamentos. A obra é uma crítica ao totalitarismo e à opressão governamental, explorando temas como vigilância em massa, manipulação histórica e controle mental.",
                "nota": 4.7,
                "capa_url": "https://m.media-amazon.com/images/I/819js3EQwbL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "Dom Quixote",
                "autor": "Miguel de Cervantes",
                "ano_publicacao": 1605,
                "genero": "Romance Clássico",
                "sinopse": "Considerado o primeiro romance moderno, narra as aventuras do fidalgo Alonso Quijano, que enlouquece após ler muitos romances de cavalaria e decide tornar-se um cavaleiro andante sob o nome de Dom Quixote de la Mancha. Acompanhado de seu fiel escudeiro Sancho Pança, ele parte em busca de aventuras, confundindo a realidade com suas fantasias.",
                "nota": 4.6,
                "capa_url": "https://m.media-amazon.com/images/I/71LGz+E+TtL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "O Pequeno Príncipe",
                "autor": "Antoine de Saint-Exupéry",
                "ano_publicacao": 1943,
                "genero": "Fábula",
                "sinopse": "Uma fábula poética que aborda temas profundos como amor, amizade, solidão e o sentido da vida. A história começa quando um aviador cai no deserto do Saara e encontra um menino misterioso, o Pequeno Príncipe, que veio de um asteroide distante. Através de suas conversas, o aviador aprende lições valiosas sobre a vida e as relações humanas.",
                "nota": 4.9,
                "capa_url": "https://m.media-amazon.com/images/I/71OZY035QKL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "Crime e Castigo",
                "autor": "Fiódor Dostoiévski",
                "ano_publicacao": 1866,
                "genero": "Romance Psicológico",
                "sinopse": "O romance acompanha a história de Raskólnikov, um ex-estudante que comete um assassinato para provar sua teoria de que pessoas extraordinárias estão acima da lei moral. A obra explora profundamente a psicologia do crime, o remorso e a redenção, além de questões filosóficas sobre moralidade, niilismo e a condição humana.",
                "nota": 4.7,
                "capa_url": "https://m.media-amazon.com/images/I/61un6+JjAUL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "Orgulho e Preconceito",
                "autor": "Jane Austen",
                "ano_publicacao": 1813,
                "genero": "Romance",
                "sinopse": "Ambientado na Inglaterra rural do século XIX, o romance narra a história de Elizabeth Bennet e sua família. A trama gira em torno dos relacionamentos e casamentos das cinco irmãs Bennet, com foco especial no relacionamento entre Elizabeth e o orgulhoso Sr. Darcy. A obra é uma crítica social à época, abordando temas como casamento, moral, educação e preconceitos de classe.",
                "nota": 4.8,
                "capa_url": "https://m.media-amazon.com/images/I/71Q1tPupKjL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "A Metamorfose",
                "autor": "Franz Kafka",
                "ano_publicacao": 1915,
                "genero": "Ficção Absurdista",
                "sinopse": "A novela conta a história de Gregor Samsa, um caixeiro-viajante que acorda certa manhã transformado em um inseto monstruoso. A obra explora temas como alienação, identidade e o absurdo da condição humana, enquanto acompanha a reação da família de Gregor à sua transformação e seu gradual abandono.",
                "nota": 4.5,
                "capa_url": "https://m.media-amazon.com/images/I/61OUBSaYJEL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "Ulisses",
                "autor": "James Joyce",
                "ano_publicacao": 1922,
                "genero": "Modernismo",
                "sinopse": "Considerada uma das obras mais importantes da literatura modernista, a narrativa acompanha um único dia na vida de Leopold Bloom em Dublin. O romance é conhecido por sua complexidade estilística, experimentação com a linguagem e referências à Odisseia de Homero. A obra explora temas como identidade irlandesa, relações humanas e a condição do homem moderno.",
                "nota": 4.4,
                "capa_url": "https://m.media-amazon.com/images/I/71QKrhhMJIL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "A Divina Comédia",
                "autor": "Dante Alighieri",
                "ano_publicacao": 1320,
                "genero": "Poema Épico",
                "sinopse": "Este poema épico narra a jornada de Dante pelos três reinos do além-túmulo: Inferno, Purgatório e Paraíso. Guiado inicialmente pelo poeta romano Virgílio e depois por sua amada Beatriz, Dante encontra figuras históricas e mitológicas, explorando temas religiosos, filosóficos e políticos da época medieval.",
                "nota": 4.6,
                "capa_url": "https://m.media-amazon.com/images/I/61Iy2SvKFPL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "Moby Dick",
                "autor": "Herman Melville",
                "ano_publicacao": 1851,
                "genero": "Aventura",
                "sinopse": "A história segue a obsessiva busca do Capitão Ahab pela baleia branca Moby Dick, que arrancou sua perna em um encontro anterior. Narrado pelo marinheiro Ishmael, o romance explora temas como obsessão, vingança, bem e mal, além de oferecer detalhes minuciosos sobre a indústria baleeira do século XIX.",
                "nota": 4.5,
                "capa_url": "https://m.media-amazon.com/images/I/71+WUTwT+ML._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "O Senhor dos Anéis",
                "autor": "J.R.R. Tolkien",
                "ano_publicacao": 1954,
                "genero": "Fantasia",
                "sinopse": "Ambientada no mundo fictício da Terra-média, a trilogia narra a jornada do hobbit Frodo Bolseiro para destruir o Um Anel, uma poderosa artefato criado pelo Senhor das Trevas Sauron. Acompanhado pela Sociedade do Anel, Frodo enfrenta perigos e desafios enquanto tenta impedir que Sauron recupere seu poder e domine a Terra-média.",
                "nota": 4.9,
                "capa_url": "https://m.media-amazon.com/images/I/71ZLavBjpRL._AC_UF1000,1000_QL80_.jpg"
            },
            {
                "titulo": "Harry Potter e a Pedra Filosofal",
                "autor": "J.K. Rowling",
                "ano_publicacao": 1997,
                "genero": "Fantasia",
                "sinopse": "O primeiro livro da série Harry Potter apresenta o jovem órfão Harry, que descobre ser um bruxo no seu décimo primeiro aniversário. Ele é convidado a estudar na Escola de Magia e Bruxaria de Hogwarts, onde faz amigos, aprende magia e descobre a verdade sobre seu passado e a ameaça do bruxo das trevas Lord Voldemort.",
                "nota": 4.8,
                "capa_url": "https://m.media-amazon.com/images/I/81ibfYk4qmL._AC_UF1000,1000_QL80_.jpg"
            }
        ]
        
        data_adicao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for livro in livros_populares:
            c.execute('''
            INSERT INTO livros (titulo, autor, ano_publicacao, genero, sinopse, nota, data_adicao, capa_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                livro["titulo"], 
                livro["autor"], 
                livro["ano_publicacao"], 
                livro["genero"], 
                livro["sinopse"], 
                livro["nota"], 
                data_adicao,
                livro["capa_url"]
            ))
            
            # Adicionar alguns comentários fictícios para cada livro
            livro_id = c.lastrowid
            
            comentarios = [
                {
                    "nome": "Leitor Entusiasta",
                    "comentario": f"Simplesmente adorei {livro['titulo']}! Uma obra-prima que me fez refletir profundamente.",
                    "data": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "nome": "Crítico Literário",
                    "comentario": f"A narrativa de {livro['autor']} é brilhante. A construção dos personagens e o desenvolvimento da trama são impecáveis.",
                    "data": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
            
            for comentario in comentarios:
                c.execute('''
                INSERT INTO comentarios (livro_id, nome_usuario, comentario, data_comentario)
                VALUES (?, ?, ?, ?)
                ''', (
                    livro_id,
                    comentario["nome"],
                    comentario["comentario"],
                    comentario["data"]
                ))
    
    conn.commit()
    conn.close()

# Função para adicionar um novo livro
def adicionar_livro(titulo, autor, ano_publicacao, genero, sinopse, nota, capa_url=""):
    """Adiciona um novo livro ao banco de dados."""
    conn = sqlite3.connect('biblioteca.db')
    c = conn.cursor()
    
    data_adicao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Se não for fornecida uma URL de capa, usar uma imagem de placeholder
    if not capa_url:
        capa_url = f"https://picsum.photos/seed/{random.randint(1, 1000)}/400/600"
    
    c.execute('''
    INSERT INTO livros (titulo, autor, ano_publicacao, genero, sinopse, nota, data_adicao, capa_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, autor, ano_publicacao, genero, sinopse, nota, data_adicao, capa_url))
    
    livro_id = c.lastrowid
    
    conn.commit()
    conn.close()
    
    return livro_id

# Função para obter todos os livros
def obter_livros():
    """Retorna todos os livros do banco de dados."""
    conn = sqlite3.connect('biblioteca.db')
    livros = pd.read_sql_query("SELECT * FROM livros ORDER BY data_adicao DESC", conn)
    conn.close()
    return livros

# Função para obter livros populares (com maior nota)
def obter_livros_populares(limite=6):
    """Retorna os livros mais bem avaliados."""
    conn = sqlite3.connect('biblioteca.db')
    livros = pd.read_sql_query(f"SELECT * FROM livros ORDER BY nota DESC LIMIT {limite}", conn)
    conn.close()
    return livros

# Função para obter um livro específico pelo ID
def obter_livro_por_id(livro_id):
    """Retorna um livro específico pelo ID."""
    conn = sqlite3.connect('biblioteca.db')
    livro = pd.read_sql_query("SELECT * FROM livros WHERE id = ?", conn, params=(livro_id,))
    conn.close()
    return livro

# Função para adicionar um comentário
def adicionar_comentario(livro_id, nome_usuario, comentario):
    """Adiciona um novo comentário a um livro."""
    conn = sqlite3.connect('biblioteca.db')
    c = conn.cursor()
    
    data_comentario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
    INSERT INTO comentarios (livro_id, nome_usuario, comentario, data_comentario)
    VALUES (?, ?, ?, ?)
    ''', (livro_id, nome_usuario, comentario, data_comentario))
    
    conn.commit()
    conn.close()

# Função para obter comentários de um livro
def obter_comentarios(livro_id):
    """Retorna todos os comentários de um livro específico."""
    conn = sqlite3.connect('biblioteca.db')
    comentarios = pd.read_sql_query(
        "SELECT * FROM comentarios WHERE livro_id = ? ORDER BY data_comentario DESC", 
        conn, 
        params=(livro_id,)
    )
    conn.close()
    return comentarios

# Função para buscar livros
def buscar_livros(termo_busca):
    """Busca livros pelo título, autor ou gênero."""
    conn = sqlite3.connect('biblioteca.db')
    termo = f"%{termo_busca}%"
    livros = pd.read_sql_query(
        "SELECT * FROM livros WHERE titulo LIKE ? OR autor LIKE ? OR genero LIKE ? ORDER BY data_adicao DESC", 
        conn, 
        params=(termo, termo, termo)
    )
    conn.close()
    return livros

# Função para renderizar estrelas baseado na nota
def renderizar_estrelas(nota):
    """Renderiza estrelas baseado na nota (0-5)."""
    estrelas_cheias = int(nota)
    meia_estrela = 1 if nota - estrelas_cheias >= 0.5 else 0
    estrelas_vazias = 5 - estrelas_cheias - meia_estrela
    
    return "⭐" * estrelas_cheias + ("⭐" if meia_estrela else "") + "☆" * estrelas_vazias

# Função para obter estatísticas
def obter_estatisticas():
    """Retorna estatísticas sobre os livros e comentários."""
    conn = sqlite3.connect('biblioteca.db')
    c = conn.cursor()
    
    # Total de livros
    c.execute("SELECT COUNT(*) FROM livros")
    total_livros = c.fetchone()[0]
    
    # Nota média
    c.execute("SELECT AVG(nota) FROM livros")
    nota_media = c.fetchone()[0] or 0
    nota_media = round(nota_media, 1)
    
    # Total de comentários
    c.execute("SELECT COUNT(*) FROM comentarios")
    total_comentarios = c.fetchone()[0]
    
    # Gêneros diferentes
    c.execute("SELECT COUNT(DISTINCT genero) FROM livros")
    total_generos = c.fetchone()[0]
    
    conn.close()
    
    return {
        "total_livros": total_livros,
        "nota_media": nota_media,
        "total_comentarios": total_comentarios,
        "total_generos": total_generos
    }

# Inicializar o banco de dados e adicionar livros populares
init_db()
adicionar_livros_populares()

# Configuração de estado da sessão
if 'pagina_atual' not in st.session_state:
    st.session_state['pagina_atual'] = 'inicio'

# Barra de navegação
with st.container():
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Início", "Explorar", "Adicionar Livro", "Sobre", "Detalhes"],
        icons=["house-fill", "search", "book-fill", "info-circle-fill", "book-half"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": f"{PRIMARY_COLOR}"},
            "icon": {"color": "white", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": f"{SECONDARY_COLOR}"},
            "nav-link-selected": {"background-color": f"{SECONDARY_COLOR}"},
        }
    )
    
    # Se o usuário clicar em "Detalhes" no menu e não tiver um livro selecionado, redirecionar para a página inicial
    if selected == "Detalhes" and 'livro_selecionado' not in st.session_state:
        selected = "Início"
    
    st.session_state['pagina_atual'] = selected.lower()
    st.markdown('</div>', unsafe_allow_html=True)

# Barra de busca
if st.session_state['pagina_atual'] in ['início', 'explorar']:
    col1, col2 = st.columns([4, 1])
    with col1:
        termo_busca = st.text_input("🔍 Buscar livros por título, autor ou gênero", "")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        buscar = st.button("Buscar")
    
    if buscar and termo_busca:
        st.session_state['termo_busca'] = termo_busca
        st.session_state['pagina_atual'] = 'resultados_busca'
        st.rerun()

# Página Inicial
if st.session_state['pagina_atual'] == 'início':
    # Banner principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="banner animate-fade-in">
            <h1>📚 BiblioTech</h1>
            <p>Sua biblioteca digital para descobrir, catalogar e compartilhar experiências literárias</p>
            <div>
                <a href="#explorar" class="banner-button">Explorar Livros</a>
                <a href="#adicionar" class="banner-button-outline">Adicionar Livro</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st_lottie(lottie_book, height=300, key="book_animation")
    
    # Estatísticas
    stats = obter_estatisticas()
    
    st.markdown('<div style="margin: 40px 0;">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card animate-fade-in delay-1">
            <div class="stats-icon"><i class="fas fa-book"></i></div>
            <div class="stats-number">{stats['total_livros']}</div>
            <div class="stats-label">Livros Catalogados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card animate-fade-in delay-2">
            <div class="stats-icon"><i class="fas fa-star"></i></div>
            <div class="stats-number">{stats['nota_media']}</div>
            <div class="stats-label">Nota Média</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card animate-fade-in delay-3">
            <div class="stats-icon"><i class="fas fa-comments"></i></div>
            <div class="stats-number">{stats['total_comentarios']}</div>
            <div class="stats-label">Comentários</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stats-card animate-fade-in delay-4">
            <div class="stats-icon"><i class="fas fa-tags"></i></div>
            <div class="stats-number">{stats['total_generos']}</div>
            <div class="stats-label">Gêneros Diferentes</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Seção de livros populares
    st.markdown('<div class="featured-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="featured-title animate-fade-in">📊 Livros Mais Populares</h2>', unsafe_allow_html=True)
    
    livros_populares = obter_livros_populares(6)
    
    # Exibir livros populares em um grid de 3 colunas
    cols = st.columns(3)
    
    for i, (_, livro) in enumerate(livros_populares.iterrows()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="book-card animate-fade-in" style="animation-delay: {i * 0.1}s">
                <img src="{livro['capa_url']}" class="book-cover" alt="Capa do livro {livro['titulo']}">
                <div class="book-title">{livro['titulo']}</div>
                <div class="book-author">por {livro['autor']}</div>
                <div class="book-meta">
                    <span>{livro['genero']}</span>
                    <span>{livro['ano_publicacao']}</span>
                </div>
                <div class="book-rating">{renderizar_estrelas(livro['nota'])}</div>
                <div class="book-description">{livro['sinopse'][:100]}...</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botão funcional do Streamlit
            if st.button(f"Ver Detalhes", key=f"btn_pop_{livro['id']}"):
                st.session_state['livro_selecionado'] = livro['id']
                st.session_state['pagina_atual'] = 'detalhes'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Seção de adições recentes
    st.markdown('<div class="featured-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="featured-title animate-fade-in">🆕 Adições Recentes</h2>', unsafe_allow_html=True)
    
    livros_recentes = obter_livros().head(3)
    
    # Exibir livros recentes em um grid de 3 colunas
    cols = st.columns(3)
    
    for i, (_, livro) in enumerate(livros_recentes.iterrows()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="book-card animate-fade-in" style="animation-delay: {i * 0.1}s">
                <img src="{livro['capa_url']}" class="book-cover" alt="Capa do livro {livro['titulo']}">
                <div class="book-title">{livro['titulo']}</div>
                <div class="book-author">por {livro['autor']}</div>
                <div class="book-meta">
                    <span>{livro['genero']}</span>
                    <span>{livro['ano_publicacao']}</span>
                </div>
                <div class="book-rating">{renderizar_estrelas(livro['nota'])}</div>
                <div class="book-description">{livro['sinopse'][:100]}...</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botão funcional do Streamlit
            if st.button(f"Ver Detalhes", key=f"btn_rec_{livro['id']}"):
                st.session_state['livro_selecionado'] = livro['id']
                st.session_state['pagina_atual'] = 'detalhes'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Página Explorar
elif st.session_state['pagina_atual'] == 'explorar':
    st.markdown('<h1 class="animate-fade-in">📚 Explorar Biblioteca</h1>', unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_genero = st.multiselect(
            "Filtrar por Gênero",
            ["Romance", "Ficção Científica", "Fantasia", "Não-Ficção", "Biografia", 
             "História", "Autoajuda", "Realismo Mágico", "Ficção Distópica", "Romance Clássico",
             "Fábula", "Romance Psicológico", "Ficção Absurdista", "Modernismo", "Poema Épico",
             "Aventura", "Outro"]
        )
    
    with col2:
        filtro_nota_min = st.slider("Nota Mínima", 0.0, 5.0, 0.0, 0.5)
    
    with col3:
        ordenar_por = st.selectbox(
            "Ordenar por",
            ["Mais Recentes", "Melhor Avaliados", "Título (A-Z)", "Autor (A-Z)", "Ano (Mais Recente)"]
        )
    
    # Obter livros e aplicar filtros
    livros = obter_livros()
    
    # Aplicar filtros
    if filtro_genero:
        livros = livros[livros['genero'].isin(filtro_genero)]
    
    livros = livros[livros['nota'] >= filtro_nota_min]
    
    # Aplicar ordenação
    if ordenar_por == "Mais Recentes":
        livros = livros.sort_values(by="data_adicao", ascending=False)
    elif ordenar_por == "Melhor Avaliados":
        livros = livros.sort_values(by="nota", ascending=False)
    elif ordenar_por == "Título (A-Z)":
        livros = livros.sort_values(by="titulo")
    elif ordenar_por == "Autor (A-Z)":
        livros = livros.sort_values(by="autor")
    elif ordenar_por == "Ano (Mais Recente)":
        livros = livros.sort_values(by="ano_publicacao", ascending=False)
    
    # Verificar se existem livros
    if livros.empty:
        st.info("Nenhum livro encontrado com os filtros selecionados.")
    else:
        # Exibir livros em um layout de grade
        st.markdown(f"<p>Exibindo {len(livros)} livros</p>", unsafe_allow_html=True)
        
        # Criar grid de 3 colunas
        cols = st.columns(3)
        
        for i, (_, livro) in enumerate(livros.iterrows()):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="book-card animate-fade-in" style="animation-delay: {i * 0.1}s">
                    <img src="{livro['capa_url']}" class="book-cover" alt="Capa do livro {livro['titulo']}">
                    <div class="book-title">{livro['titulo']}</div>
                    <div class="book-author">por {livro['autor']}</div>
                    <div class="book-meta">
                        <span>{livro['genero']}</span>
                        <span>{livro['ano_publicacao']}</span>
                    </div>
                    <div class="book-rating">{renderizar_estrelas(livro['nota'])}</div>
                    <div class="book-description">{livro['sinopse'][:100]}...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Botão funcional do Streamlit
                if st.button(f"Ver Detalhes", key=f"btn_exp_{livro['id']}"):
                    st.session_state['livro_selecionado'] = livro['id']
                    st.session_state['pagina_atual'] = 'detalhes'
                    st.rerun()

# Página de Resultados de Busca
elif st.session_state['pagina_atual'] == 'resultados_busca':
    termo_busca = st.session_state.get('termo_busca', '')
    st.markdown(f'<h1 class="animate-fade-in">🔍 Resultados para "{termo_busca}"</h1>', unsafe_allow_html=True)
    
    # Obter resultados da busca
    livros = buscar_livros(termo_busca)
    
    # Verificar se existem resultados
    if livros.empty:
        st.info(f"Nenhum livro encontrado para '{termo_busca}'.")
        if st.button("← Voltar"):
            st.session_state['pagina_atual'] = 'início'
            st.rerun()
    else:
        # Exibir resultados em um layout de grade
        st.markdown(f"<p>Encontrados {len(livros)} livros</p>", unsafe_allow_html=True)
        
        # Criar grid de 3 colunas
        cols = st.columns(3)
        
        for i, (_, livro) in enumerate(livros.iterrows()):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="book-card animate-fade-in" style="animation-delay: {i * 0.1}s">
                    <img src="{livro['capa_url']}" class="book-cover" alt="Capa do livro {livro['titulo']}">
                    <div class="book-title">{livro['titulo']}</div>
                    <div class="book-author">por {livro['autor']}</div>
                    <div class="book-meta">
                        <span>{livro['genero']}</span>
                        <span>{livro['ano_publicacao']}</span>
                    </div>
                    <div class="book-rating">{renderizar_estrelas(livro['nota'])}</div>
                    <div class="book-description">{livro['sinopse'][:100]}...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Botão funcional do Streamlit
                if st.button(f"Ver Detalhes", key=f"btn_search_{livro['id']}"):
                    st.session_state['livro_selecionado'] = livro['id']
                    st.session_state['pagina_atual'] = 'detalhes'
                    st.rerun()

# Página Adicionar Livro
elif st.session_state['pagina_atual'] == 'adicionar livro':
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<h1 class="animate-fade-in">📝 Adicionar Novo Livro</h1>', unsafe_allow_html=True)
    
    with col2:
        st_lottie(lottie_reading, height=150, key="reading_animation")
    
    # Formulário para adicionar livro
    with st.form(key="adicionar_livro_form", clear_on_submit=True):
        st.markdown('<div class="form-container animate-fade-in">', unsafe_allow_html=True)
        st.markdown('<h3 class="form-title">Informações do Livro</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            titulo = st.text_input("Título*")
            autor = st.text_input("Autor*")
            ano_publicacao = st.number_input("Ano de Publicação", min_value=1000, max_value=datetime.now().year, value=2023)
        
        with col2:
            genero = st.selectbox("Gênero", [
                "Romance", "Ficção Científica", "Fantasia", "Não-Ficção", "Biografia", 
                "História", "Autoajuda", "Realismo Mágico", "Ficção Distópica", "Romance Clássico",
                "Fábula", "Romance Psicológico", "Ficção Absurdista", "Modernismo", "Poema Épico",
                "Aventura", "Outro"
            ])
            nota = st.slider("Nota", 0.0, 5.0, 4.0, 0.5)
            capa_url = st.text_input("URL da Capa (opcional)", "")
        
        sinopse = st.text_area("Sinopse", height=150)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit_button = st.form_submit_button(label="Adicionar Livro")
        with col2:
            st.markdown("""
            <div style="height: 38px; display: flex; align-items: center; justify-content: flex-end;">
                <span style="color: #64748b; font-size: 0.9rem;">* Campos obrigatórios</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submit_button:
            if not titulo or not autor:
                st.error("Título e autor são campos obrigatórios!")
            else:
                novo_id = adicionar_livro(titulo, autor, ano_publicacao, genero, sinopse, nota, capa_url)
                st.success(f"Livro '{titulo}' adicionado com sucesso!")
                
                # Mostrar o livro adicionado
                st.session_state['livro_selecionado'] = novo_id
                st.session_state['pagina_atual'] = 'detalhes'
                st.rerun()

# Página Sobre
elif st.session_state['pagina_atual'] == 'sobre':
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<h1 class="animate-fade-in">ℹ️ Sobre o BiblioTech</h1>', unsafe_allow_html=True)
    
    with col2:
        st_lottie(lottie_library, height=150, key="library_animation")
    
    st.markdown("""
    <div class="book-detail-container animate-fade-in glass-card">
        <h2 style="color: #7c3aed; margin-bottom: 20px;">Bem-vindo ao BiblioTech!</h2>
        
        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;">
            O BiblioTech é uma aplicação web moderna desenvolvida inteiramente em Python usando Streamlit, 
            projetada para ajudar os amantes de livros a catalogar, descobrir e compartilhar experiências literárias.
        </p>
        
        <h3 style="color: #7c3aed; margin-top: 30px; margin-bottom: 15px;">Principais Funcionalidades</h3>
        
        <ul style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;">
            <li><strong>Catálogo de Livros:</strong> Adicione e gerencie sua coleção de livros com informações detalhadas.</li>
            <li><strong>Sistema de Avaliação:</strong> Avalie livros com notas de 0 a 5 estrelas.</li>
            <li><strong>Comentários:</strong> Compartilhe suas opiniões e leia comentários de outros usuários.</li>
            <li><strong>Busca e Filtros:</strong> Encontre facilmente livros por título, autor ou gênero.</li>
            <li><strong>Interface Responsiva:</strong> Design moderno e adaptável a diferentes dispositivos.</li>
        </ul>
        
        <h3 style="color: #7c3aed; margin-top: 30px; margin-bottom: 15px;">Tecnologias Utilizadas</h3>
        
        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;">
            Esta aplicação foi desenvolvida utilizando:
        </p>
        
        <ul style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;">
            <li><strong>Python:</strong> Linguagem de programação principal.</li>
            <li><strong>Streamlit:</strong> Framework para criação de aplicações web interativas.</li>
            <li><strong>SQLite:</strong> Banco de dados leve para armazenamento de informações.</li>
            <li><strong>Pandas:</strong> Biblioteca para manipulação e análise de dados.</li>
            <li><strong>CSS Personalizado:</strong> Para estilização avançada da interface.</li>
            <li><strong>Lottie:</strong> Para animações interativas.</li>
        </ul>
        
        <h3 style="color: #7c3aed; margin-top: 30px; margin-bottom: 15px;">Sobre o Desenvolvedor</h3>
        
        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;">
            O BiblioTech foi desenvolvido como um projeto demonstrativo para mostrar as capacidades do Python
            na criação de aplicações web completas e visualmente atraentes, sem a necessidade de HTML, CSS ou JavaScript diretos.
        </p>
        
        <div style="text-align: center; margin-top: 40px; color: #64748b;">
            <p>© 2023 BiblioTech - Todos os direitos reservados</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Página de Detalhes do Livro
elif st.session_state['pagina_atual'] == 'detalhes':
    # Verificar se existe um livro selecionado
    if 'livro_selecionado' in st.session_state:
        livro_id = st.session_state['livro_selecionado']
        livro_df = obter_livro_por_id(livro_id)
        
        if not livro_df.empty:
            livro = livro_df.iloc[0]
            
            # Botão para voltar
            if st.button("← Voltar à Lista de Livros"):
                # Manter o livro selecionado, mas voltar para a página anterior
                pagina_anterior = st.session_state.get('pagina_anterior', 'início')
                st.session_state['pagina_atual'] = pagina_anterior
                st.rerun()
            
            # Container de detalhes do livro
            st.markdown('<div class="book-detail-container animate-fade-in">', unsafe_allow_html=True)
            
            # Layout de duas colunas para detalhes do livro
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <img src="{livro['capa_url']}" class="book-detail-cover" alt="Capa do livro {livro['titulo']}">
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="book-detail-title">{livro['titulo']}</div>
                <div class="book-detail-author">por {livro['autor']}</div>
                <div class="book-detail-meta">
                    <span><strong>Gênero:</strong> {livro['genero']}</span>
                    <span><strong>Ano:</strong> {livro['ano_publicacao']}</span>
                    <span><strong>Adicionado em:</strong> {livro['data_adicao'][:10]}</span>
                </div>
                <div class="book-detail-rating">{renderizar_estrelas(livro['nota'])} ({livro['nota']})</div>
                """, unsafe_allow_html=True)
            
            # Sinopse
            st.markdown(f"""
            <h3 style="margin-top: 30px; color: {PRIMARY_COLOR};">Sinopse</h3>
            <div class="book-detail-synopsis">{livro['sinopse']}</div>
            """, unsafe_allow_html=True)
            
            # Seção de comentários
            st.markdown(f"""
            <div class="comment-section">
                <h3 style="color: {PRIMARY_COLOR};">Comentários</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Formulário para adicionar comentário
            with st.form(key=f"comentario_form_{livro_id}", clear_on_submit=True):
                st.markdown('<h4 style="color: #7c3aed;">Adicionar Comentário</h4>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    nome_usuario = st.text_input("Seu Nome")
                
                with col2:
                    comentario = st.text_area("Seu Comentário", height=100)
                
                submit_comentario = st.form_submit_button(label="Enviar Comentário")
                
                if submit_comentario:
                    if not nome_usuario or not comentario:
                        st.error("Por favor, preencha todos os campos!")
                    else:
                        adicionar_comentario(livro_id, nome_usuario, comentario)
                        st.success("Comentário adicionado com sucesso!")
                        st.rerun()
            
            # Exibir comentários existentes
            comentarios = obter_comentarios(livro_id)
            
            if comentarios.empty:
                st.info("Ainda não há comentários para este livro. Seja o primeiro a comentar!")
            else:
                for _, comentario in comentarios.iterrows():
                    st.markdown(f"""
                    <div class="comment-box">
                        <div class="comment-author">{comentario['nome_usuario']}</div>
                        <div class="comment-date">{comentario['data_comentario']}</div>
                        <div class="comment-content">{comentario['comentario']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Livro não encontrado!")
            st.session_state['pagina_atual'] = 'início'
            st.rerun()
    else:
        st.error("Nenhum livro selecionado!")
        st.session_state['pagina_atual'] = 'início'
        st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>© 2023 BiblioTech - Desenvolvido com ❤️ usando Python e Streamlit</p>
</div>
""", unsafe_allow_html=True)
