import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd
import logging
from models import Base, Livro

# Configuração de logging
logger = logging.getLogger(__name__)

# Configuração do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL')

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Função para inicializar o banco de dados
def init_db():
    Base.metadata.create_all(engine)
    logger.info("Tabelas do banco de dados criadas")

# Função para importar dados do CSV para o banco de dados (se necessário)
def import_from_csv(csv_path='livros.csv'):
    session = Session()
    try:
        # Verifica se já existem livros no banco de dados
        existing_count = session.query(Livro).count()
        
        if existing_count == 0 and os.path.exists(csv_path):
            logger.info(f"Importando dados do arquivo CSV: {csv_path}")
            try:
                # Lê o CSV
                df = pd.read_csv(csv_path)
                
                # Para cada linha no dataframe, cria um objeto Livro e adiciona à sessão
                for _, row in df.iterrows():
                    livro = Livro(
                        titulo=row['Título'],
                        autor=row['Autor'],
                        genero=row['Gênero'],
                        ano=int(row['Ano']),
                        avaliacao=int(row['Avaliação']) if pd.notna(row['Avaliação']) and row['Avaliação'] != '' else None,
                        opiniao=row['Opinião'] if pd.notna(row['Opinião']) and row['Opinião'] != '' else None
                    )
                    session.add(livro)
                
                # Commit das alterações
                session.commit()
                logger.info(f"Importados {len(df)} livros do CSV para o banco de dados")
            except Exception as e:
                session.rollback()
                logger.error(f"Erro ao importar dados do CSV: {e}")
        else:
            logger.info("Pular importação: o banco de dados já contém registros ou o CSV não existe")
    finally:
        session.close()

# Função para obter todos os livros do banco de dados
def get_all_books():
    session = Session()
    try:
        livros = session.query(Livro).all()
        return [livro.to_dict() for livro in livros]
    finally:
        session.close()

# Função para adicionar um novo livro
def add_book(titulo, autor, genero, ano):
    session = Session()
    try:
        novo_livro = Livro(
            titulo=titulo,
            autor=autor,
            genero=genero,
            ano=int(ano),
            avaliacao=None,
            opiniao=None
        )
        session.add(novo_livro)
        session.commit()
        logger.debug(f"Livro adicionado: {titulo} por {autor}")
        return novo_livro.to_dict()
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao adicionar livro: {e}")
        raise
    finally:
        session.close()

# Função para obter um livro pelo ID
def get_book_by_id(livro_id):
    session = Session()
    try:
        livro = session.query(Livro).filter(Livro.id == livro_id).first()
        if livro:
            return livro.to_dict()
        return None
    finally:
        session.close()

# Função para atualizar a avaliação e opinião de um livro
def update_book_rating(livro_id, avaliacao, opiniao):
    session = Session()
    try:
        livro = session.query(Livro).filter(Livro.id == livro_id).first()
        if livro:
            livro.avaliacao = avaliacao
            livro.opiniao = opiniao
            session.commit()
            logger.debug(f"Livro ID {livro_id} atualizado com avaliação {avaliacao}")
            return True
        return False
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao atualizar avaliação do livro: {e}")
        raise
    finally:
        session.close()

# Inicializa o banco de dados e importa dados se necessário
def setup_database():
    init_db()
    import_from_csv()