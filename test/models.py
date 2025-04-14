from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Livro(Base):
    __tablename__ = 'livros'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(String(255), nullable=False)
    genero = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)
    avaliacao = Column(Integer, nullable=True)
    opiniao = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Livro(titulo='{self.titulo}', autor='{self.autor}', ano={self.ano})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'Título': self.titulo,
            'Autor': self.autor,
            'Gênero': self.genero,
            'Ano': self.ano,
            'Avaliação': str(self.avaliacao) if self.avaliacao is not None else '',
            'Opinião': self.opiniao if self.opiniao is not None else ''
        }