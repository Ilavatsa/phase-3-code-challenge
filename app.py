from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    articles = relationship("Article", back_populates="author")

class Magazine(Base):
    __tablename__ = 'magazines'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String)

    articles = relationship("Article", back_populates="magazine")

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    magazine_id = Column(Integer, ForeignKey('magazines.id'))

    author = relationship("Author", back_populates="articles")
    magazine = relationship("Magazine", back_populates="articles")

def main():
    # Connect to the database
    engine = create_engine('sqlite:///sample.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Insert data into the database
    author = Author(name=author_name)
    magazine = Magazine(name=magazine_name, category=magazine_category)
    article = Article(title=article_title, content=article_content, author=author, magazine=magazine)

    session.add(author)
    session.add(magazine)
    session.add(article)
    session.commit()

    # Display inserted records
    print("\nAuthors:")
    for author in session.query(Author).all():
        print(author)

    print("\nMagazines:")
    for magazine in session.query(Magazine).all():
        print(magazine)

    print("\nArticles:")
    for article in session.query(Article).all():
        print(article)

    session.close()

if __name__ == "__main__":
    main()
